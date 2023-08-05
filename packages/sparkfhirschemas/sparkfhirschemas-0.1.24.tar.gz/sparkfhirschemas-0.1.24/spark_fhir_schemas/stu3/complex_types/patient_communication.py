from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Patient_CommunicationSchema:
    """
    Demographics and other administrative information about an individual or
    animal receiving care or other health-related services.
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
        Demographics and other administrative information about an individual or
        animal receiving care or other health-related services.


        language: The ISO-639-1 alpha 2 code in lower case for the language, optionally followed
            by a hyphen and the ISO-3166-1 alpha 2 code for the region in upper case; e.g.
            "en" for English, or "en-US" for American English versus "en-EN" for England
            English.

        preferred: Indicates whether or not the patient prefers this language (over other
            languages he masters up a certain level).

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("Patient_Communication") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Patient_Communication"]
        schema = StructType(
            [
                # The ISO-639-1 alpha 2 code in lower case for the language, optionally followed
                # by a hyphen and the ISO-3166-1 alpha 2 code for the region in upper case; e.g.
                # "en" for English, or "en-US" for American English versus "en-EN" for England
                # English.
                StructField(
                    "language",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Indicates whether or not the patient prefers this language (over other
                # languages he masters up a certain level).
                StructField("preferred", BooleanType(), True),
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
