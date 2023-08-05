# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Specker JSON Specification Validator,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import typing

class SpecContent:
    """Spec Content Container
    """

    _name:str
    _required:bool
    _default:typing.Any
    _type:str
    _comment:str
    _example:str
    _values:list[typing.Any]

    def get(self,attr:str) -> typing.Any:
        """Get a Parameter
        @param str \c attr Attribute to Get
        @retval Any Value of Attribute if it exists
        @throws AttributeError Cannot find Requested Attribute (or not set)
        """
        if not hasattr(self,f"_{attr}"):
            raise AttributeError(f"Unable to locate {attr}")
        return getattr(self,f"_{attr}")

    __type_map:dict[str,object] = {
        "str": str,
        "int": int,
        "list": list,
        "dict": dict,
        "bool": bool,
        "any": typing.Any,
        "float": float
    }

    @property
    def type(self) -> object:
        """Get Spec Value Type
        @retval type Type specified from Spec
        """
        return self.__type_map[self._type]

    def __init__(self,content:dict[str,typing.Any]) -> None:
        """Initializer
        @param dict[str,typing.Any] \c content Spec Content
        """
        for k,v in content.items():
            setattr(self,f"_{k}",v)
        if not hasattr(self,"_name"):
            raise ValueError("Spec is missing required attribute: name")
        if not hasattr(self,"_type"):
            raise ValueError("Spec is missing required attribute: type")
        if self._type not in self.__type_map.keys():
            raise ValueError("Spec has invalid type option. See Documentation for valid options for 'type'")
        if not hasattr(self,"_required"):
            self._required = False
        if not hasattr(self,"_default"):
            self._default = None
        if not hasattr(self,"_comment"):
            self._comment = ""
        if not hasattr(self,"_example"):
            self._example = ""
        if not hasattr(self,"_values"):
            self._values = []

    def __str__(self) -> str:
        """To String Generator
        @retval str Markdown Formatted Data about Spec
        """
        default_str:str = ""
        if self._default is not None:
            default_str = f"\n - Default: {str(self._default)}"
        values_str:str = ""
        if len(self._values) > 0:
            values_str = f"\n - Acceptable Values: {', '.join(self._values)}"
        example_str:str = ""
        if len(self._example) > 0:
            example_str = f"\n - Example: {str(self._example)}"
        return f'''Option: `{self._name}` - {self._comment}
 - Type: {self._type}
 - Required: {str(self._required)}{default_str}{values_str}{example_str}
'''
