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
class GoalSchema:
    """
    Describes the intended objective(s) for a patient, group or organization care,
    for example, weight loss, restoring an activity of daily living, obtaining
    herd immunity via immunization, meeting a process improvement objective, etc.
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
        Describes the intended objective(s) for a patient, group or organization care,
        for example, weight loss, restoring an activity of daily living, obtaining
        herd immunity via immunization, meeting a process improvement objective, etc.


        resourceType: This is a Goal resource

        identifier: This records identifiers associated with this care plan that are defined by
            business processes and/or used to refer to it when a direct URL reference to
            the resource itself is not appropriate (e.g. in CDA documents, or in written /
            printed documentation).

        status: Indicates whether the goal has been reached and is still considered relevant.

        category: Indicates a category the goal falls within.

        priority: Identifies the mutually agreed level of importance associated with
            reaching/sustaining the goal.

        description: Human-readable and/or coded description of a specific desired objective of
            care, such as "control blood pressure" or "negotiate an obstacle course" or
            "dance with child at wedding".

        subject: Identifies the patient, group or organization for whom the goal is being
            established.

        startDate: The date or event after which the goal should begin being pursued.

        startCodeableConcept: The date or event after which the goal should begin being pursued.

        target: Indicates what should be done by when.

        statusDate: Identifies when the current status.  I.e. When initially created, when
            achieved, when cancelled, etc.

        statusReason: Captures the reason for the current status.

        expressedBy: Indicates whose goal this is - patient goal, practitioner goal, etc.

        addresses: The identified conditions and other health record elements that are intended
            to be addressed by the goal.

        note: Any comments related to the goal.

        outcomeCode: Identifies the change (or lack of change) at the point when the status of the
            goal is assessed.

        outcomeReference: Details of what's changed (or not changed).

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.goal_target import Goal_TargetSchema
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema

        if (
            max_recursion_limit and nesting_list.count("Goal") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Goal"]
        schema = StructType(
            [
                # This is a Goal resource
                StructField("resourceType", StringType(), True),
                # This records identifiers associated with this care plan that are defined by
                # business processes and/or used to refer to it when a direct URL reference to
                # the resource itself is not appropriate (e.g. in CDA documents, or in written /
                # printed documentation).
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
                # Indicates whether the goal has been reached and is still considered relevant.
                StructField("status", StringType(), True),
                # Indicates a category the goal falls within.
                StructField(
                    "category",
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
                # Identifies the mutually agreed level of importance associated with
                # reaching/sustaining the goal.
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
                # Human-readable and/or coded description of a specific desired objective of
                # care, such as "control blood pressure" or "negotiate an obstacle course" or
                # "dance with child at wedding".
                StructField(
                    "description",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Identifies the patient, group or organization for whom the goal is being
                # established.
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
                # The date or event after which the goal should begin being pursued.
                StructField("startDate", StringType(), True),
                # The date or event after which the goal should begin being pursued.
                StructField(
                    "startCodeableConcept",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Indicates what should be done by when.
                StructField(
                    "target",
                    Goal_TargetSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Identifies when the current status.  I.e. When initially created, when
                # achieved, when cancelled, etc.
                StructField("statusDate", StringType(), True),
                # Captures the reason for the current status.
                StructField("statusReason", StringType(), True),
                # Indicates whose goal this is - patient goal, practitioner goal, etc.
                StructField(
                    "expressedBy",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The identified conditions and other health record elements that are intended
                # to be addressed by the goal.
                StructField(
                    "addresses",
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
                # Any comments related to the goal.
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
                # Identifies the change (or lack of change) at the point when the status of the
                # goal is assessed.
                StructField(
                    "outcomeCode",
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
                # Details of what's changed (or not changed).
                StructField(
                    "outcomeReference",
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
