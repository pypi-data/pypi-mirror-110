from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Immunization_ExplanationSchema:
    """
    Describes the event of a patient being administered a vaccination or a record
    of a vaccination as reported by a patient, a clinician or another party and
    may include vaccine reaction information and what vaccination protocol was
    followed.
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
        Describes the event of a patient being administered a vaccination or a record
        of a vaccination as reported by a patient, a clinician or another party and
        may include vaccine reaction information and what vaccination protocol was
        followed.


        reason: Reasons why a vaccine was administered.

        reasonNotGiven: Reason why a vaccine was not administered.

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("Immunization_Explanation") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Immunization_Explanation"]
        schema = StructType(
            [
                # Reasons why a vaccine was administered.
                StructField(
                    "reason",
                    ArrayType(
                        CodeableConceptSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Reason why a vaccine was not administered.
                StructField(
                    "reasonNotGiven",
                    ArrayType(
                        CodeableConceptSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
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
