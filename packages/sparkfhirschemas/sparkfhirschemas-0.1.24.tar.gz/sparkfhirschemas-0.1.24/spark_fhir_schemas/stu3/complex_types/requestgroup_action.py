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
class RequestGroup_ActionSchema:
    """
    A group of related requests that can be used to capture intended activities
    that have inter-dependencies such as "give this medication after that one".
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
        A group of related requests that can be used to capture intended activities
        that have inter-dependencies such as "give this medication after that one".


        label: A user-visible label for the action.

        title: The title of the action displayed to a user.

        description: A short description of the action used to provide a summary to display to the
            user.

        textEquivalent: A text equivalent of the action to be performed. This provides a human-
            interpretable description of the action when the definition is consumed by a
            system that may not be capable of interpreting it dynamically.

        code: A code that provides meaning for the action or action group. For example, a
            section may have a LOINC code for a the section of a documentation template.

        documentation: Didactic or other informational resources associated with the action that can
            be provided to the CDS recipient. Information resources can include inline
            text commentary and links to web resources.

        condition: An expression that describes applicability criteria, or start/stop conditions
            for the action.

        relatedAction: A relationship to another action such as "before" or "30-60 minutes after
            start of".

        timingDateTime: An optional value describing when the action should be performed.

        timingPeriod: An optional value describing when the action should be performed.

        timingDuration: An optional value describing when the action should be performed.

        timingRange: An optional value describing when the action should be performed.

        timingTiming: An optional value describing when the action should be performed.

        participant: The participant that should perform or be responsible for this action.

        type: The type of action to perform (create, update, remove).

        groupingBehavior: Defines the grouping behavior for the action and its children.

        selectionBehavior: Defines the selection behavior for the action and its children.

        requiredBehavior: Defines the requiredness behavior for the action.

        precheckBehavior: Defines whether the action should usually be preselected.

        cardinalityBehavior: Defines whether the action can be selected multiple times.

        resource: The resource that is the target of the action (e.g. CommunicationRequest).

        action: Sub actions.

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.relatedartifact import (
            RelatedArtifactSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.requestgroup_condition import (
            RequestGroup_ConditionSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.requestgroup_relatedaction import (
            RequestGroup_RelatedActionSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.duration import DurationSchema
        from spark_fhir_schemas.stu3.complex_types.range import RangeSchema
        from spark_fhir_schemas.stu3.complex_types.timing import TimingSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.coding import CodingSchema

        if (
            max_recursion_limit
            and nesting_list.count("RequestGroup_Action") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["RequestGroup_Action"]
        schema = StructType(
            [
                # A user-visible label for the action.
                StructField("label", StringType(), True),
                # The title of the action displayed to a user.
                StructField("title", StringType(), True),
                # A short description of the action used to provide a summary to display to the
                # user.
                StructField("description", StringType(), True),
                # A text equivalent of the action to be performed. This provides a human-
                # interpretable description of the action when the definition is consumed by a
                # system that may not be capable of interpreting it dynamically.
                StructField("textEquivalent", StringType(), True),
                # A code that provides meaning for the action or action group. For example, a
                # section may have a LOINC code for a the section of a documentation template.
                StructField(
                    "code",
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
                # Didactic or other informational resources associated with the action that can
                # be provided to the CDS recipient. Information resources can include inline
                # text commentary and links to web resources.
                StructField(
                    "documentation",
                    ArrayType(
                        RelatedArtifactSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # An expression that describes applicability criteria, or start/stop conditions
                # for the action.
                StructField(
                    "condition",
                    ArrayType(
                        RequestGroup_ConditionSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # A relationship to another action such as "before" or "30-60 minutes after
                # start of".
                StructField(
                    "relatedAction",
                    ArrayType(
                        RequestGroup_RelatedActionSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # An optional value describing when the action should be performed.
                StructField("timingDateTime", StringType(), True),
                # An optional value describing when the action should be performed.
                StructField(
                    "timingPeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # An optional value describing when the action should be performed.
                StructField(
                    "timingDuration",
                    DurationSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # An optional value describing when the action should be performed.
                StructField(
                    "timingRange",
                    RangeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # An optional value describing when the action should be performed.
                StructField(
                    "timingTiming",
                    TimingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The participant that should perform or be responsible for this action.
                StructField(
                    "participant",
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
                # The type of action to perform (create, update, remove).
                StructField(
                    "type",
                    CodingSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Defines the grouping behavior for the action and its children.
                StructField("groupingBehavior", StringType(), True),
                # Defines the selection behavior for the action and its children.
                StructField("selectionBehavior", StringType(), True),
                # Defines the requiredness behavior for the action.
                StructField("requiredBehavior", StringType(), True),
                # Defines whether the action should usually be preselected.
                StructField("precheckBehavior", StringType(), True),
                # Defines whether the action can be selected multiple times.
                StructField("cardinalityBehavior", StringType(), True),
                # The resource that is the target of the action (e.g. CommunicationRequest).
                StructField(
                    "resource",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Sub actions.
                StructField(
                    "action",
                    ArrayType(
                        RequestGroup_ActionSchema.get_schema(
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
