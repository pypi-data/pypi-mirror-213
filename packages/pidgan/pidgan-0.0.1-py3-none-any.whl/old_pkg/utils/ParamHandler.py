import json


class ParamHandler:
  def __init__ ( self, **kwargs ) -> None:
    self._params = dict (**kwargs) 
    self._used_keys = set()

  def update ( self, **kwargs ) -> None:
    for key in kwargs.keys():
      if key in self._used_keys: 
        raise KeyError ( f"The parameter {key} was already used and is now read-only" )
    self._params.update ( kwargs )

  def get ( self, key, default ) -> dict:
    if key not in self._params.keys(): self._params [ key ] = default
    self._used_keys.add ( key ) 
    return self._params [ key ]

  def clean ( self ) -> None:
    self._params = dict() 
    self._used_keys = set()

  def __del__ ( self ) -> None: 
    for key in self._params.keys():
      if key not in self._used_keys:
        print ( f"[WARNING] The parameter {key} was defined but never used" ) 
        print ( self._used_keys ) 

  def __str__ ( self ) -> str:
    import pprint 
    return pprint.pformat ( self._params )

  def get_dict ( self ) -> dict:
    return dict ( **self._params ) 

  def dump ( self, filename ) -> None:
    with open ( filename, "w" ) as fp:
      json.dump ( self._params, fp ) 


__PARAMETERS__ = None 

def getInstance() -> ParamHandler:
  global __PARAMETERS__
  if __PARAMETERS__ is None: __PARAMETERS__ = ParamHandler()
  return __PARAMETERS__
