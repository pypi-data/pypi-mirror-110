from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class CodeSystem_PropertySchema:
    """
    A code system resource specifies a set of codes drawn from one or more code
    systems.
    """

    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False,
    ) -> Union[StructType, DataType]:
        """
        A code system resource specifies a set of codes drawn from one or more code
        systems.


        code: A code that is used to identify the property. The code is used internally (in
            CodeSystem.concept.property.code) and also externally, such as in property
            filters.

        uri: Reference to the formal meaning of the property. One possible source of
            meaning is the [Concept Properties](codesystem-concept-properties.html) code
            system.

        description: A description of the property- why it is defined, and how its value might be
            used.

        type: The type of the property value. Properties of type "code" contain a code
            defined by the code system (e.g. a reference to anotherr defined concept).

        """
        if (
            max_recursion_limit
            and nesting_list.count("CodeSystem_Property") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["CodeSystem_Property"]
        schema = StructType(
            [
                # A code that is used to identify the property. The code is used internally (in
                # CodeSystem.concept.property.code) and also externally, such as in property
                # filters.
                StructField("code", StringType(), True),
                # Reference to the formal meaning of the property. One possible source of
                # meaning is the [Concept Properties](codesystem-concept-properties.html) code
                # system.
                StructField("uri", StringType(), True),
                # A description of the property- why it is defined, and how its value might be
                # used.
                StructField("description", StringType(), True),
                # The type of the property value. Properties of type "code" contain a code
                # defined by the code system (e.g. a reference to anotherr defined concept).
                StructField("type", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c
                if c.name != "extension"
                else StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
