from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Specimen_CollectionSchema:
    """
    A sample to be used for analysis.
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
        A sample to be used for analysis.


        collector: Person who collected the specimen.

        collectedDateTime: Time when specimen was collected from subject - the physiologically relevant
            time.

        collectedPeriod: Time when specimen was collected from subject - the physiologically relevant
            time.

        quantity: The quantity of specimen collected; for instance the volume of a blood sample,
            or the physical measurement of an anatomic pathology sample.

        method: A coded value specifying the technique that is used to perform the procedure.

        bodySite: Anatomical location from which the specimen was collected (if subject is a
            patient). This is the target site.  This element is not used for environmental
            specimens.

        """
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("Specimen_Collection") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Specimen_Collection"]
        schema = StructType(
            [
                # Person who collected the specimen.
                StructField(
                    "collector",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Time when specimen was collected from subject - the physiologically relevant
                # time.
                StructField("collectedDateTime", StringType(), True),
                # Time when specimen was collected from subject - the physiologically relevant
                # time.
                StructField(
                    "collectedPeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The quantity of specimen collected; for instance the volume of a blood sample,
                # or the physical measurement of an anatomic pathology sample.
                StructField(
                    "quantity",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # A coded value specifying the technique that is used to perform the procedure.
                StructField(
                    "method",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Anatomical location from which the specimen was collected (if subject is a
                # patient). This is the target site.  This element is not used for environmental
                # specimens.
                StructField(
                    "bodySite",
                    CodeableConceptSchema.get_schema(
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
