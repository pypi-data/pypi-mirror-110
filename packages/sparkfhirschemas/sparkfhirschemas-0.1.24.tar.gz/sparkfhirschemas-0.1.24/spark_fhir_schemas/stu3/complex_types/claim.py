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
class ClaimSchema:
    """
    A provider issued list of services and products provided, or to be provided,
    to a patient which is provided to an insurer for payment recovery.
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
        A provider issued list of services and products provided, or to be provided,
        to a patient which is provided to an insurer for payment recovery.


        resourceType: This is a Claim resource

        identifier: The business identifier for the instance: claim number, pre-determination or
            pre-authorization number.

        status: The status of the resource instance.

        type: The category of claim, eg, oral, pharmacy, vision, insitutional, professional.

        subType: A finer grained suite of claim subtype codes which may convey Inpatient vs
            Outpatient and/or a specialty service. In the US the BillType.

        use: Complete (Bill or Claim), Proposed (Pre-Authorization), Exploratory (Pre-
            determination).

        patient: Patient Resource.

        billablePeriod: The billable period for which charges are being submitted.

        created: The date when the enclosed suite of services were performed or completed.

        enterer: Person who created the invoice/claim/pre-determination or pre-authorization.

        insurer: The Insurer who is target of the request.

        provider: The provider which is responsible for the bill, claim pre-determination, pre-
            authorization.

        organization: The organization which is responsible for the bill, claim pre-determination,
            pre-authorization.

        priority: Immediate (STAT), best effort (NORMAL), deferred (DEFER).

        fundsReserve: In the case of a Pre-Determination/Pre-Authorization the provider may request
            that funds in the amount of the expected Benefit be reserved ('Patient' or
            'Provider') to pay for the Benefits determined on the subsequent claim(s).
            'None' explicitly indicates no funds reserving is requested.

        related: Other claims which are related to this claim such as prior claim versions or
            for related services.

        prescription: Prescription to support the dispensing of Pharmacy or Vision products.

        originalPrescription: Original prescription which has been superceded by this prescription to
            support the dispensing of pharmacy services, medications or products. For
            example, a physician may prescribe a medication which the pharmacy determines
            is contraindicated, or for which the patient has an intolerance, and therefor
            issues a new precription for an alternate medication which has the same
            theraputic intent. The prescription from the pharmacy becomes the
            'prescription' and that from the physician becomes the 'original
            prescription'.

        payee: The party to be reimbursed for the services.

        referral: The referral resource which lists the date, practitioner, reason and other
            supporting information.

        facility: Facility where the services were provided.

        careTeam: The members of the team who provided the overall service as well as their role
            and whether responsible and qualifications.

        information: Additional information codes regarding exceptions, special considerations, the
            condition, situation, prior or concurrent issues. Often there are mutiple
            jurisdiction specific valuesets which are required.

        diagnosis: List of patient diagnosis for which care is sought.

        procedure: Ordered list of patient procedures performed to support the adjudication.

        insurance: Financial instrument by which payment information for health care.

        accident: An accident which resulted in the need for healthcare services.

        employmentImpacted: The start and optional end dates of when the patient was precluded from
            working due to the treatable condition(s).

        hospitalization: The start and optional end dates of when the patient was confined to a
            treatment center.

        item: First tier of goods and services.

        total: The total value of the claim.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.claim_related import (
            Claim_RelatedSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_payee import Claim_PayeeSchema
        from spark_fhir_schemas.stu3.complex_types.claim_careteam import (
            Claim_CareTeamSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_information import (
            Claim_InformationSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_diagnosis import (
            Claim_DiagnosisSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_procedure import (
            Claim_ProcedureSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_insurance import (
            Claim_InsuranceSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_accident import (
            Claim_AccidentSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.claim_item import Claim_ItemSchema
        from spark_fhir_schemas.stu3.complex_types.money import MoneySchema

        if (
            max_recursion_limit and nesting_list.count("Claim") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Claim"]
        schema = StructType(
            [
                # This is a Claim resource
                StructField("resourceType", StringType(), True),
                # The business identifier for the instance: claim number, pre-determination or
                # pre-authorization number.
                StructField(
                    "identifier",
                    ArrayType(
                        IdentifierSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # The status of the resource instance.
                StructField("status", StringType(), True),
                # The category of claim, eg, oral, pharmacy, vision, insitutional, professional.
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
                # A finer grained suite of claim subtype codes which may convey Inpatient vs
                # Outpatient and/or a specialty service. In the US the BillType.
                StructField(
                    "subType",
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
                # Complete (Bill or Claim), Proposed (Pre-Authorization), Exploratory (Pre-
                # determination).
                StructField("use", StringType(), True),
                # Patient Resource.
                StructField(
                    "patient",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The billable period for which charges are being submitted.
                StructField(
                    "billablePeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The date when the enclosed suite of services were performed or completed.
                StructField("created", StringType(), True),
                # Person who created the invoice/claim/pre-determination or pre-authorization.
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
                # The Insurer who is target of the request.
                StructField(
                    "insurer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The provider which is responsible for the bill, claim pre-determination, pre-
                # authorization.
                StructField(
                    "provider",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The organization which is responsible for the bill, claim pre-determination,
                # pre-authorization.
                StructField(
                    "organization",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Immediate (STAT), best effort (NORMAL), deferred (DEFER).
                StructField(
                    "priority",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # In the case of a Pre-Determination/Pre-Authorization the provider may request
                # that funds in the amount of the expected Benefit be reserved ('Patient' or
                # 'Provider') to pay for the Benefits determined on the subsequent claim(s).
                # 'None' explicitly indicates no funds reserving is requested.
                StructField(
                    "fundsReserve",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Other claims which are related to this claim such as prior claim versions or
                # for related services.
                StructField(
                    "related",
                    ArrayType(
                        Claim_RelatedSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Prescription to support the dispensing of Pharmacy or Vision products.
                StructField(
                    "prescription",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Original prescription which has been superceded by this prescription to
                # support the dispensing of pharmacy services, medications or products. For
                # example, a physician may prescribe a medication which the pharmacy determines
                # is contraindicated, or for which the patient has an intolerance, and therefor
                # issues a new precription for an alternate medication which has the same
                # theraputic intent. The prescription from the pharmacy becomes the
                # 'prescription' and that from the physician becomes the 'original
                # prescription'.
                StructField(
                    "originalPrescription",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The party to be reimbursed for the services.
                StructField(
                    "payee",
                    Claim_PayeeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The referral resource which lists the date, practitioner, reason and other
                # supporting information.
                StructField(
                    "referral",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Facility where the services were provided.
                StructField(
                    "facility",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The members of the team who provided the overall service as well as their role
                # and whether responsible and qualifications.
                StructField(
                    "careTeam",
                    ArrayType(
                        Claim_CareTeamSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Additional information codes regarding exceptions, special considerations, the
                # condition, situation, prior or concurrent issues. Often there are mutiple
                # jurisdiction specific valuesets which are required.
                StructField(
                    "information",
                    ArrayType(
                        Claim_InformationSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # List of patient diagnosis for which care is sought.
                StructField(
                    "diagnosis",
                    ArrayType(
                        Claim_DiagnosisSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Ordered list of patient procedures performed to support the adjudication.
                StructField(
                    "procedure",
                    ArrayType(
                        Claim_ProcedureSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Financial instrument by which payment information for health care.
                StructField(
                    "insurance",
                    ArrayType(
                        Claim_InsuranceSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # An accident which resulted in the need for healthcare services.
                StructField(
                    "accident",
                    Claim_AccidentSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The start and optional end dates of when the patient was precluded from
                # working due to the treatable condition(s).
                StructField(
                    "employmentImpacted",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The start and optional end dates of when the patient was confined to a
                # treatment center.
                StructField(
                    "hospitalization",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # First tier of goods and services.
                StructField(
                    "item",
                    ArrayType(
                        Claim_ItemSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # The total value of the claim.
                StructField(
                    "total",
                    MoneySchema.get_schema(
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
