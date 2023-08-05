from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ValueSet_FilterSchema:
    """
    A value set specifies a set of codes drawn from one or more code systems.
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
        A value set specifies a set of codes drawn from one or more code systems.


        property: A code that identifies a property defined in the code system.

        op: The kind of operation to perform as a part of the filter criteria.

        value: The match value may be either a code defined by the system, or a string value,
            which is a regex match on the literal string of the property value when the
            operation is 'regex', or one of the values (true and false), when the
            operation is 'exists'.

        """
        if (
            max_recursion_limit
            and nesting_list.count("ValueSet_Filter") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ValueSet_Filter"]
        schema = StructType(
            [
                # A code that identifies a property defined in the code system.
                StructField("property", StringType(), True),
                # The kind of operation to perform as a part of the filter criteria.
                StructField("op", StringType(), True),
                # The match value may be either a code defined by the system, or a string value,
                # which is a regex match on the literal string of the property value when the
                # operation is 'regex', or one of the values (true and false), when the
                # operation is 'exists'.
                StructField("value", StringType(), True),
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
