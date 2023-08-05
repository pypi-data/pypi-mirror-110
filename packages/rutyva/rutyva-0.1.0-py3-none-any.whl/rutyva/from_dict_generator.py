from typing import Optional, get_origin, get_args, Union, Literal, Any


def get_subclass_if_in_list(parent_class: type, subclass_subst: Optional[list[tuple[type, type]]]):
  if subclass_subst is None: return parent_class
  filtered_class = [t[1] for t in subclass_subst if t[0] == parent_class]
  if len(filtered_class) == 0: return parent_class
  return filtered_class[0]

def check_subclasses(subclasses_subs: list[tuple[type, type]]):
  for class_pair in subclasses_subs:
    raise_if_is_not_type(class_pair[0])
    raise_if_is_not_type(class_pair[1])
    raise_if_not_subclass(class_pair[0], class_pair[1])

def raise_if_not_subclass(parent_cls: type, child_cls: type):
  if not issubclass(child_cls, parent_cls):
    raise TypeError(f'{child_cls.__name__} is not a subclass of {parent_cls.__name__}')

def raise_if_is_not_type(cls):
  if not isinstance(cls, type):
    raise TypeError(f'{cls} is not a class!')

def gen_from_any(d_val, ann, subclass_subst):
  origin = get_origin(ann)
  if origin is not None:
    if origin == list:
      return gen_from_list(d_val, get_args(ann)[0], subclass_subst)
    if origin == Union:
      return gen_from_union(d_val, get_args(ann), subclass_subst)
    if origin == Literal: #(int, bool, str, bytes, None)
      return d_val
    if origin == tuple:
      return gen_from_tuple(d_val, get_args(ann), subclass_subst)
    if origin == dict:
      return gen_from_dict(d_val, get_args(ann), subclass_subst)

    print('GENERATION WITH ORIGIN NOT IMPLEMENTED:', ann, origin, d_val)
    return d_val
  else:
    if isinstance(d_val, ann):
      return d_val
    if ann == Any:
      return d_val

    # check if has from_dict class method
    subst_subclass_or_class = get_subclass_if_in_list(ann, subclass_subst)
    from_dict_method = getattr(subst_subclass_or_class, 'from_dict', None)
    if from_dict_method is not None:
      return from_dict_method(d_val)
    
    try:
      return subst_subclass_or_class(**d_val)
    except:
      return d_val

def gen_from_list(d_val, ann, subclass_subst):
  if not isinstance(d_val, list): return d_val

  gen_list = []
  for obj in d_val:
    gen_list.append(gen_from_any(obj, ann, subclass_subst))
  
  return gen_list

def gen_from_tuple(d_val, anns, subclass_subst):
  if not isinstance(d_val, (tuple, list)): return d_val

  anns_len = len(anns)
  d_val_len = len(d_val)

  if anns_len != d_val_len: return d_val

  gen_lis = []
  for i in range(len(anns)):
    gen_lis.append(gen_from_any(d_val[i], anns[i], subclass_subst))

  return tuple(gen_lis)

def gen_from_union(d_val, anns, subclass_subst):
  for ann in anns:
    try:
      new_val = gen_from_any(d_val, ann, subclass_subst)
    except:
      new_val = d_val
    
    if d_val != new_val:
      return new_val
  
  return d_val

def gen_from_dict(d_val, amns, subclass_subst):
  if not isinstance(d_val, dict): return d_val
  new_dict = {}
  key_class = amns[0]
  val_class = amns[1]

  for val in d_val:
    new_key = gen_from_any(val, key_class, subclass_subst) #needs to be hashable (int, bool, str, tuple)
    new_val = gen_from_any(d_val[val], val_class, subclass_subst)
    try:
      new_dict[new_key] = new_val
    except:
      return d_val

  return new_dict