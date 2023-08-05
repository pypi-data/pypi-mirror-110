from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ElementDefinition_DiscriminatorSchema:
    """
    Captures constraints on each element within the resource, profile, or
    extension.
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
        Captures constraints on each element within the resource, profile, or
        extension.


        type: How the element value is interpreted when discrimination is evaluated.

        path: A FHIRPath expression, using a restricted subset of FHIRPath, that is used to
            identify the element on which discrimination is based.

        """
        if (
            max_recursion_limit
            and nesting_list.count("ElementDefinition_Discriminator")
            >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ElementDefinition_Discriminator"]
        schema = StructType(
            [
                # How the element value is interpreted when discrimination is evaluated.
                StructField("type", StringType(), True),
                # A FHIRPath expression, using a restricted subset of FHIRPath, that is used to
                # identify the element on which discrimination is based.
                StructField("path", StringType(), True),
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
