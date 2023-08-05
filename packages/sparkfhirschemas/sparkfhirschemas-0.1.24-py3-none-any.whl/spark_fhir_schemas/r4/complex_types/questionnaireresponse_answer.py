from typing import Union, List, Optional

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    DateType,
    BooleanType,
    IntegerType,
    DataType,
    FloatType,
    TimestampType,
)


# This file is auto-generated by generate_schema so do not edit it manually
# noinspection PyPep8Naming
class QuestionnaireResponse_AnswerSchema:
    """
    A structured set of questions and their answers. The questions are ordered and
    grouped into coherent subsets, corresponding to the structure of the grouping
    of the questionnaire being responded to.
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
        A structured set of questions and their answers. The questions are ordered and
        grouped into coherent subsets, corresponding to the structure of the grouping
        of the questionnaire being responded to.


        id: Unique id for the element within a resource (for internal references). This
            may be any string value that does not contain spaces.

        extension: May be used to represent additional information that is not part of the basic
            definition of the element. To make the use of extensions safe and manageable,
            there is a strict set of governance  applied to the definition and use of
            extensions. Though any implementer can define an extension, there is a set of
            requirements that SHALL be met as part of the definition of the extension.

        valueBoolean: The answer (or one of the answers) provided by the respondent to the question.

        valueDecimal: The answer (or one of the answers) provided by the respondent to the question.

        valueInteger: The answer (or one of the answers) provided by the respondent to the question.

        valueDate: The answer (or one of the answers) provided by the respondent to the question.

        valueDateTime: The answer (or one of the answers) provided by the respondent to the question.

        valueTime: The answer (or one of the answers) provided by the respondent to the question.

        valueString: The answer (or one of the answers) provided by the respondent to the question.

        valueUri: The answer (or one of the answers) provided by the respondent to the question.

        valueAttachment: The answer (or one of the answers) provided by the respondent to the question.

        valueCoding: The answer (or one of the answers) provided by the respondent to the question.

        valueQuantity: The answer (or one of the answers) provided by the respondent to the question.

        valueReference: The answer (or one of the answers) provided by the respondent to the question.

        item: Nested groups and/or questions found within this particular answer.

        """
        from spark_fhir_schemas.r4.complex_types.extension import ExtensionSchema
        from spark_fhir_schemas.r4.complex_types.attachment import AttachmentSchema
        from spark_fhir_schemas.r4.complex_types.coding import CodingSchema
        from spark_fhir_schemas.r4.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.r4.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.r4.complex_types.questionnaireresponse_item import (
            QuestionnaireResponse_ItemSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("QuestionnaireResponse_Answer")
            >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["QuestionnaireResponse_Answer"]
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
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueBoolean", BooleanType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueDecimal", FloatType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueInteger", IntegerType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueDate", DateType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueDateTime", TimestampType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueTime", StringType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueString", StringType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueUri", StringType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField(
                    "valueAttachment",
                    AttachmentSchema.get_schema(
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
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField(
                    "valueCoding",
                    CodingSchema.get_schema(
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
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField(
                    "valueQuantity",
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
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField(
                    "valueReference",
                    ReferenceSchema.get_schema(
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
                # Nested groups and/or questions found within this particular answer.
                StructField(
                    "item",
                    ArrayType(
                        QuestionnaireResponse_ItemSchema.get_schema(
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
