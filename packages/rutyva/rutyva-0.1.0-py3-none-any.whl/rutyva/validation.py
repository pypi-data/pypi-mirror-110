from typing import Any, Literal, Union, get_args, get_origin

def validate_var(var: Any, ann: Any) -> None:
  '''
  Validate if the variable type is the expected by the annotation
  '''
  origin = get_origin(ann)
  if origin is not None:
    return validate_with_origin(origin, var, get_args(ann))

  return validate_without_origin(var, ann)

def validate_without_origin(var: Any, ann: Any) -> None:
  ann_to_test = ann if ann != float else (int, float)

  if ann_to_test == Any: return

  if not isinstance(var, ann_to_test):
    raise TypeError(format_type_error(var, ann))
  
def validate_with_origin(origin: Any, var: Any, args: tuple) -> None:
    if origin == Union:
      return validate_union(var, args)
    if origin == Literal:
      return validate_literal(var, args)
    if origin == list:
      return validate_list(var, args[0])
    if origin == tuple:
      return validate_tuple(var, args)
    if origin == dict:
      return validate_dict(var, args)

    print('VALIDATION WITH ORIGIN NOT IMPLEMENTED:', var, args, origin)

def validate_dict(var: Any, anns: tuple) -> None:
  if not isinstance(var, dict):
    raise TypeError(format_type_error(var, dict))

  key_class = anns[0]
  val_class = anns[1]
  for key in var:
    try:
      validate_var(key, key_class)
    except Exception as e:
      raise TypeError(f'dict key ' + e.args[0])

    try:
      validate_var(var[key], val_class)
    except Exception as e:
      raise TypeError(f'dict key ({key}) -> value ' + e.args[0])

def validate_literal(var: Any, options: tuple) -> None:
  if var not in options:
    raise TypeError(f'({var}) is not one of the valid options: ({options})')

def validate_union(var: Any, anns: tuple) -> None:
  for ann in anns:
    try:
      validate_var(var, ann)
      return
    except:
      pass
  
  anns_str = format_ann_args(anns, 'union')
  error_message = f'({var}) is ({type(var).__name__}), but should be ({anns_str})'
  raise TypeError(error_message)

def validate_tuple(var: Any, anns: tuple) -> None:
  if not isinstance(var, tuple):
    raise TypeError(format_type_error(var, tuple))
  
  var_len = len(var)
  anns_len = len(anns)
  if var_len != anns_len:
    raise TypeError(f'tuple with length {var_len}, should have length {anns_len}')

  for i in range(anns_len):
    try:
      validate_var(var[i], anns[i])
    except Exception as e:
      raise(TypeError(f'error in position ({i}): ' + e.args[0]))

def validate_list(var: Any, ann: Any) -> None:
  if not isinstance(var, list):
    raise TypeError(format_type_error(var, list))
  
  for i in range(len(var)):
    try:
      validate_var(var[i], ann)
    except Exception as e:
      raise TypeError(f'error in position ({i}): '+e.args[0])

def format_type_error(var, ann) -> str:
  return f'({var}) is ({type(var).__name__}), but should be ({ann.__name__})'

def format_ann_args(ann_args, origin_type: str) -> str:
  if not isinstance(ann_args, tuple):
    return ann_args.__name__

  anns_str = ''
  count_anns = len(ann_args)
  for i in range(count_anns):
    ann_arg = ann_args[i]
    origin = get_origin(ann_arg)
    anns_str_prefix = ann_arg.__name__

    if origin is not None:
      if origin == tuple:
        anns_str_prefix += '[' + format_ann_args(get_args(ann_arg), 'tuple')+ ']'
      if origin == list:
        anns_str_prefix += '[' + get_args(ann_arg)[0].__name__ + ']'
      if origin == dict:
        anns_str_prefix += '[' + format_ann_args(get_args(ann_arg), 'dict')+ ']'
      # if origin == Union:
      #   anns_str_prefix = format_ann_args(get_args(ann_arg), 'union')


    if i == count_anns-1:
      anns_str += anns_str_prefix
    else:
      if origin_type == 'union':
        anns_str += anns_str_prefix + ' | '
      # elif origin_type == 'tuple':
      else:
        anns_str += anns_str_prefix + ', '

  return anns_str