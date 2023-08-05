from typing import Union, List, Optional

from pyspark.sql.types import StructType, StringType, DataType


# This file is auto-generated by generate_schema so do not edit it manually
# noinspection PyPep8Naming
class idSchema:
    """
    Any combination of letters, numerals, "-" and ".", with a length limit of 64
    characters.  (This might be an integer, an unprefixed OID, UUID or any other
    identifier pattern that meets these constraints.)  Ids are case-insensitive.
    """

    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False,
        extension_fields: Optional[List[str]] = [
            "valueBoolean",
            "valueCode",
            "valueDate",
            "valueDateTime",
            "valueDecimal",
            "valueId",
            "valueInteger",
            "valuePositiveInt",
            "valueString",
            "valueTime",
            "valueUnsignedInt",
            "valueUri",
            "valueUrl",
        ],
        extension_depth: int = 0,
        max_extension_depth: Optional[int] = 2,
    ) -> Union[StructType, DataType]:
        """
        Any combination of letters, numerals, "-" and ".", with a length limit of 64
        characters.  (This might be an integer, an unprefixed OID, UUID or any other
        identifier pattern that meets these constraints.)  Ids are case-insensitive.


        """
        return StringType()
