from copy import deepcopy
from dataclasses import dataclass, asdict
from typing import Optional
from .validation import validate_var
from .from_dict_generator import check_subclasses, gen_from_any


@dataclass
class BaseModel:
  def __post_init__(self):
    self.__pre_validation__()
    self.validate_attributes()
    self.__post_validation__()
  
  def __pre_validation__(self): pass

  def __post_validation__(self): pass

  def to_dict(self):
    return asdict(self)

  def validate_attributes(self, raise_error=True, return_error_message=False):
    dc_fields = self.__dataclass_fields__
    for dc_field_key in dc_fields:
      if dc_fields[dc_field_key].init:
        ann = dc_fields[dc_field_key].type
        att = self.__getattribute__(dc_field_key)
        try:
          validate_var(att, ann)
        except Exception as e:
          error_message = f'({self.__class__.__name__}) -> attribute ({dc_field_key}) -> ' + e.args[0]
          if raise_error: raise TypeError(error_message)
          if return_error_message: return error_message
          return False
    
    if not raise_error: return True

  @classmethod
  def from_dict(cls, d: dict, raise_if_extra_attribute=False, subclass_subst: Optional[list[tuple[type, type]]]=None):
    if not isinstance(d, dict): raise TypeError('Input is not a dict!')
    if subclass_subst is not None:
      check_subclasses(subclass_subst)
    d_copy = deepcopy(d)
    d_return = dict()

    dc_fields = cls.__dataclass_fields__  # type: ignore
    for key in d:
      if key not in dc_fields:
        if raise_if_extra_attribute:
          raise TypeError(f'{key} is not an attribute of {cls.__name__}')
      else:
        if dc_fields[key].init:
          try:
            d_return[key] = gen_from_any(d_copy[key], dc_fields[key].type, subclass_subst)
          except Exception as e:
            error_message = f'({cls.__name__}) attribute ({key}) of type ' + e.args[0]
            raise TypeError(error_message)
      
    # try to create missing attributes (maybe they have default values)
    # for key in dc_fields:
    #   if key not in d_return:
    #     try:
    #       key_class = dc_fields[key].type
    #       d_return[key] = key_class()
    #     except:
    #       raise TypeError(f'{cls.__name__} attribute {key} is missing')

    return cls(**d_return) # type: ignore

    #list -> get_list=None, get_args=()
    #list[Any] -> get_origin=list, get_args=(Any,)
    #list[T] -> get_origin=list, get_args=(T,)
    #list[X, Y] -> Considerar só X
