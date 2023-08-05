from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ChargeItemSchema:
    """
    The resource ChargeItem describes the provision of healthcare provider
    products for a certain patient, therefore referring not only to the product,
    but containing in addition details of the provision, like date, time, amounts
    and participating organizations and persons. Main Usage of the ChargeItem is
    to enable the billing process and internal cost allocation.
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
        The resource ChargeItem describes the provision of healthcare provider
        products for a certain patient, therefore referring not only to the product,
        but containing in addition details of the provision, like date, time, amounts
        and participating organizations and persons. Main Usage of the ChargeItem is
        to enable the billing process and internal cost allocation.


        resourceType: This is a ChargeItem resource

        identifier: Identifiers assigned to this event performer or other systems.

        definition: References the source of pricing information, rules of application for the
            code this ChargeItem uses.

        status: The current state of the ChargeItem.

        partOf: ChargeItems can be grouped to larger ChargeItems covering the whole set.

        code: A code that identifies the charge, like a billing code.

        subject: The individual or set of individuals the action is being or was performed on.

        context: The encounter or episode of care that establishes the context for this event.

        occurrenceDateTime: Date/time(s) or duration when the charged service was applied.

        occurrencePeriod: Date/time(s) or duration when the charged service was applied.

        occurrenceTiming: Date/time(s) or duration when the charged service was applied.

        participant: Indicates who or what performed or participated in the charged service.

        performingOrganization: The organization requesting the service.

        requestingOrganization: The organization performing the service.

        quantity: Quantity of which the charge item has been serviced.

        bodysite: The anatomical location where the related service has been applied.

        factorOverride: Factor overriding the factor determined by the rules associated with the code.

        priceOverride: Total price of the charge overriding the list price associated with the code.

        overrideReason: If the list price or the rule based factor associated with the code is
            overridden, this attribute can capture a text to indicate the  reason for this
            action.

        enterer: The device, practitioner, etc. who entered the charge item.

        enteredDate: Date the charge item was entered.

        reason: Describes why the event occurred in coded or textual form.

        service: Indicated the rendered service that caused this charge.

        account: Account into which this ChargeItems belongs.

        note: Comments made about the event by the performer, subject or other participants.

        supportingInformation: Further information supporting the this charge.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.timing import TimingSchema
        from spark_fhir_schemas.stu3.complex_types.chargeitem_participant import (
            ChargeItem_ParticipantSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.money import MoneySchema
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema

        if (
            max_recursion_limit
            and nesting_list.count("ChargeItem") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ChargeItem"]
        schema = StructType(
            [
                # This is a ChargeItem resource
                StructField("resourceType", StringType(), True),
                # Identifiers assigned to this event performer or other systems.
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
                # References the source of pricing information, rules of application for the
                # code this ChargeItem uses.
                # The current state of the ChargeItem.
                StructField("status", StringType(), True),
                # ChargeItems can be grouped to larger ChargeItems covering the whole set.
                StructField(
                    "partOf",
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
                # A code that identifies the charge, like a billing code.
                StructField(
                    "code",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The individual or set of individuals the action is being or was performed on.
                StructField(
                    "subject",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The encounter or episode of care that establishes the context for this event.
                StructField(
                    "context",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Date/time(s) or duration when the charged service was applied.
                StructField("occurrenceDateTime", StringType(), True),
                # Date/time(s) or duration when the charged service was applied.
                StructField(
                    "occurrencePeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Date/time(s) or duration when the charged service was applied.
                StructField(
                    "occurrenceTiming",
                    TimingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Indicates who or what performed or participated in the charged service.
                StructField(
                    "participant",
                    ArrayType(
                        ChargeItem_ParticipantSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # The organization requesting the service.
                StructField(
                    "performingOrganization",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The organization performing the service.
                StructField(
                    "requestingOrganization",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Quantity of which the charge item has been serviced.
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
                # The anatomical location where the related service has been applied.
                StructField(
                    "bodysite",
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
                # Factor overriding the factor determined by the rules associated with the code.
                StructField("factorOverride", IntegerType(), True),
                # Total price of the charge overriding the list price associated with the code.
                StructField(
                    "priceOverride",
                    MoneySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # If the list price or the rule based factor associated with the code is
                # overridden, this attribute can capture a text to indicate the  reason for this
                # action.
                StructField("overrideReason", StringType(), True),
                # The device, practitioner, etc. who entered the charge item.
                StructField(
                    "enterer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Date the charge item was entered.
                StructField("enteredDate", StringType(), True),
                # Describes why the event occurred in coded or textual form.
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
                # Indicated the rendered service that caused this charge.
                StructField(
                    "service",
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
                # Account into which this ChargeItems belongs.
                StructField(
                    "account",
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
                # Comments made about the event by the performer, subject or other participants.
                StructField(
                    "note",
                    ArrayType(
                        AnnotationSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Further information supporting the this charge.
                StructField(
                    "supportingInformation",
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
