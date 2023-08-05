from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Contract_FriendlySchema:
    """
    A formal agreement between parties regarding the conduct of business, exchange
    of information or other matters.
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
        A formal agreement between parties regarding the conduct of business, exchange
        of information or other matters.


        contentAttachment: Human readable rendering of this Contract in a format and representation
            intended to enhance comprehension and ensure understandability.

        contentReference: Human readable rendering of this Contract in a format and representation
            intended to enhance comprehension and ensure understandability.

        """
        from spark_fhir_schemas.stu3.complex_types.attachment import AttachmentSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema

        if (
            max_recursion_limit
            and nesting_list.count("Contract_Friendly") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Contract_Friendly"]
        schema = StructType(
            [
                # Human readable rendering of this Contract in a format and representation
                # intended to enhance comprehension and ensure understandability.
                StructField(
                    "contentAttachment",
                    AttachmentSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Human readable rendering of this Contract in a format and representation
                # intended to enhance comprehension and ensure understandability.
                StructField(
                    "contentReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
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
