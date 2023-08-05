from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
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
    ) -> Union[StructType, DataType]:
        """
        A structured set of questions and their answers. The questions are ordered and
        grouped into coherent subsets, corresponding to the structure of the grouping
        of the questionnaire being responded to.


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
        from spark_fhir_schemas.stu3.complex_types.attachment import AttachmentSchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.questionnaireresponse_item import (
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
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueBoolean", BooleanType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueDecimal", IntegerType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueInteger", IntegerType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueDate", StringType(), True),
                # The answer (or one of the answers) provided by the respondent to the question.
                StructField("valueDateTime", StringType(), True),
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
