from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class SupplyDelivery_SuppliedItemSchema:
    """
    Record of delivery of what is supplied.
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
        Record of delivery of what is supplied.


        quantity: The amount of supply that has been dispensed. Includes unit of measure.

        itemCodeableConcept: Identifies the medication, substance or device being dispensed. This is either
            a link to a resource representing the details of the item or a code that
            identifies the item from a known list.

        itemReference: Identifies the medication, substance or device being dispensed. This is either
            a link to a resource representing the details of the item or a code that
            identifies the item from a known list.

        """
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema

        if (
            max_recursion_limit
            and nesting_list.count("SupplyDelivery_SuppliedItem") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["SupplyDelivery_SuppliedItem"]
        schema = StructType(
            [
                # The amount of supply that has been dispensed. Includes unit of measure.
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
                # Identifies the medication, substance or device being dispensed. This is either
                # a link to a resource representing the details of the item or a code that
                # identifies the item from a known list.
                StructField(
                    "itemCodeableConcept",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Identifies the medication, substance or device being dispensed. This is either
                # a link to a resource representing the details of the item or a code that
                # identifies the item from a known list.
                StructField(
                    "itemReference",
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
