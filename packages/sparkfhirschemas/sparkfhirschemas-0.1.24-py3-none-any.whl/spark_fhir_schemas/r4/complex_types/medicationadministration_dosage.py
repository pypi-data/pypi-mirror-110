from typing import Union, List, Optional

from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DataType


# This file is auto-generated by generate_schema so do not edit it manually
# noinspection PyPep8Naming
class MedicationAdministration_DosageSchema:
    """
    Describes the event of a patient consuming or otherwise being administered a
    medication.  This may be as simple as swallowing a tablet or it may be a long
    running infusion.  Related resources tie this event to the authorizing
    prescription, and the specific encounter between patient and health care
    practitioner.
    """

    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False,
        extension_fields: Optional[List[str]] = [
            "valueBoolean",
            "valueCode",
            "valueDate",
            "valueDateTime",
            "valueDecimal",
            "valueId",
            "valueInteger",
            "valuePositiveInt",
            "valueString",
            "valueTime",
            "valueUnsignedInt",
            "valueUri",
            "valueUrl",
        ],
        extension_depth: int = 0,
        max_extension_depth: Optional[int] = 2,
    ) -> Union[StructType, DataType]:
        """
        Describes the event of a patient consuming or otherwise being administered a
        medication.  This may be as simple as swallowing a tablet or it may be a long
        running infusion.  Related resources tie this event to the authorizing
        prescription, and the specific encounter between patient and health care
        practitioner.


        id: Unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        text: Free text dosage can be used for cases where the dosage administered is too
            complex to code. When coded dosage is present, the free text dosage may still
            be present for display to humans.

            The dosage instructions should reflect the dosage of the medication that was
            administered.

        site: A coded specification of the anatomic site where the medication first entered
            the body.  For example, "left arm".

        route: A code specifying the route or physiological path of administration of a
            therapeutic agent into or onto the patient.  For example, topical,
            intravenous, etc.

        method: A coded value indicating the method by which the medication is intended to be
            or was introduced into or on the body.  This attribute will most often NOT be
            populated.  It is most commonly used for injections.  For example, Slow Push,
            Deep IV.

        dose: The amount of the medication given at one administration event.   Use this
            value when the administration is essentially an instantaneous event such as a
            swallowing a tablet or giving an injection.

        rateRatio: Identifies the speed with which the medication was or will be introduced into
            the patient.  Typically, the rate for an infusion e.g. 100 ml per 1 hour or
            100 ml/hr.  May also be expressed as a rate per unit of time, e.g. 500 ml per
            2 hours.  Other examples:  200 mcg/min or 200 mcg/1 minute; 1 liter/8 hours.

        rateQuantity: Identifies the speed with which the medication was or will be introduced into
            the patient.  Typically, the rate for an infusion e.g. 100 ml per 1 hour or
            100 ml/hr.  May also be expressed as a rate per unit of time, e.g. 500 ml per
            2 hours.  Other examples:  200 mcg/min or 200 mcg/1 minute; 1 liter/8 hours.

        """
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.r4.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.r4.complex_types.ratio import RatioSchema

        if (
            max_recursion_limit
            and nesting_list.count("MedicationAdministration_Dosage")
            >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["MedicationAdministration_Dosage"]
        schema = StructType(
            [
                # Unique id for the element within a resource (for internal references). This
                # may be any string value that does not contain spaces.
                StructField("id", StringType(), True),
                # May be used to represent additional information that is not part of the basic
                # definition of the element. To make the use of extensions safe and manageable,
                # there is a strict set of governance  applied to the definition and use of
                # extensions. Though any implementer can define an extension, there is a set of
                # requirements that SHALL be met as part of the definition of the extension.
                StructField(
                    "extension",
                    ArrayType(
                        ExtensionSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                            extension_fields=extension_fields,
                            extension_depth=extension_depth,
                            max_extension_depth=max_extension_depth,
                        )
                    ),
                    True,
                ),
                # Free text dosage can be used for cases where the dosage administered is too
                # complex to code. When coded dosage is present, the free text dosage may still
                # be present for display to humans.
                #
                # The dosage instructions should reflect the dosage of the medication that was
                # administered.
                StructField("text", StringType(), True),
                # A coded specification of the anatomic site where the medication first entered
                # the body.  For example, "left arm".
                StructField(
                    "site",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # A code specifying the route or physiological path of administration of a
                # therapeutic agent into or onto the patient.  For example, topical,
                # intravenous, etc.
                StructField(
                    "route",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # A coded value indicating the method by which the medication is intended to be
                # or was introduced into or on the body.  This attribute will most often NOT be
                # populated.  It is most commonly used for injections.  For example, Slow Push,
                # Deep IV.
                StructField(
                    "method",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # The amount of the medication given at one administration event.   Use this
                # value when the administration is essentially an instantaneous event such as a
                # swallowing a tablet or giving an injection.
                StructField(
                    "dose",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # Identifies the speed with which the medication was or will be introduced into
                # the patient.  Typically, the rate for an infusion e.g. 100 ml per 1 hour or
                # 100 ml/hr.  May also be expressed as a rate per unit of time, e.g. 500 ml per
                # 2 hours.  Other examples:  200 mcg/min or 200 mcg/1 minute; 1 liter/8 hours.
                StructField(
                    "rateRatio",
                    RatioSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
                    ),
                    True,
                ),
                # Identifies the speed with which the medication was or will be introduced into
                # the patient.  Typically, the rate for an infusion e.g. 100 ml per 1 hour or
                # 100 ml/hr.  May also be expressed as a rate per unit of time, e.g. 500 ml per
                # 2 hours.  Other examples:  200 mcg/min or 200 mcg/1 minute; 1 liter/8 hours.
                StructField(
                    "rateQuantity",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                        extension_fields=extension_fields,
                        extension_depth=extension_depth + 1,
                        max_extension_depth=max_extension_depth,
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
