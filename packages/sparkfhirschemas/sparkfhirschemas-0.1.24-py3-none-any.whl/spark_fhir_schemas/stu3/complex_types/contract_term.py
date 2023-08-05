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
class Contract_TermSchema:
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


        identifier: Unique identifier for this particular Contract Provision.

        issued: When this Contract Provision was issued.

        applies: Relevant time or time-period when this Contract Provision is applicable.

        type: Type of Contract Provision such as specific requirements, purposes for
            actions, obligations, prohibitions, e.g. life time maximum benefit.

        subType: Subtype of this Contract Provision, e.g. life time maximum payment for a
            contract term for specific valued item, e.g. disability payment.

        topic: The matter of concern in the context of this provision of the agrement.

        action: Action stipulated by this Contract Provision.

        actionReason: Reason or purpose for the action stipulated by this Contract Provision.

        securityLabel: A set of security labels that define which terms are controlled by this
            condition.

        agent: An actor taking a role in an activity for which it can be assigned some degree
            of responsibility for the activity taking place.

        text: Human readable form of this Contract Provision.

        valuedItem: Contract Provision Valued Item List.

        group: Nested group of Contract Provisions.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema
        from spark_fhir_schemas.stu3.complex_types.contract_agent1 import (
            Contract_Agent1Schema,
        )
        from spark_fhir_schemas.stu3.complex_types.contract_valueditem1 import (
            Contract_ValuedItem1Schema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("Contract_Term") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Contract_Term"]
        schema = StructType(
            [
                # Unique identifier for this particular Contract Provision.
                StructField(
                    "identifier",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # When this Contract Provision was issued.
                StructField("issued", StringType(), True),
                # Relevant time or time-period when this Contract Provision is applicable.
                StructField(
                    "applies",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Type of Contract Provision such as specific requirements, purposes for
                # actions, obligations, prohibitions, e.g. life time maximum benefit.
                StructField(
                    "type",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Subtype of this Contract Provision, e.g. life time maximum payment for a
                # contract term for specific valued item, e.g. disability payment.
                StructField(
                    "subType",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The matter of concern in the context of this provision of the agrement.
                StructField(
                    "topic",
                    ArrayType(
                        ReferenceSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Action stipulated by this Contract Provision.
                StructField(
                    "action",
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
                # Reason or purpose for the action stipulated by this Contract Provision.
                StructField(
                    "actionReason",
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
                # A set of security labels that define which terms are controlled by this
                # condition.
                StructField(
                    "securityLabel",
                    ArrayType(
                        CodingSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # An actor taking a role in an activity for which it can be assigned some degree
                # of responsibility for the activity taking place.
                StructField(
                    "agent",
                    ArrayType(
                        Contract_Agent1Schema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Human readable form of this Contract Provision.
                StructField("text", StringType(), True),
                # Contract Provision Valued Item List.
                StructField(
                    "valuedItem",
                    ArrayType(
                        Contract_ValuedItem1Schema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Nested group of Contract Provisions.
                StructField(
                    "group",
                    ArrayType(
                        Contract_TermSchema.get_schema(
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
