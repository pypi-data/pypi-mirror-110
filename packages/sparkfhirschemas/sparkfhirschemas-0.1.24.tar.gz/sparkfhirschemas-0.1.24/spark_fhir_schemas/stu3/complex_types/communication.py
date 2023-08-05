from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class CommunicationSchema:
    """
    An occurrence of information being transmitted; e.g. an alert that was sent to
    a responsible provider, a public health agency was notified about a reportable
    condition.
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
        An occurrence of information being transmitted; e.g. an alert that was sent to
        a responsible provider, a public health agency was notified about a reportable
        condition.


        resourceType: This is a Communication resource

        identifier: Identifiers associated with this Communication that are defined by business
            processes and/ or used to refer to it when a direct URL reference to the
            resource itself is not appropriate (e.g. in CDA documents, or in written /
            printed documentation).

        definition: A protocol, guideline, or other definition that was adhered to in whole or in
            part by this communication event.

        basedOn: An order, proposal or plan fulfilled in whole or in part by this
            Communication.

        partOf: Part of this action.

        status: The status of the transmission.

        notDone: If true, indicates that the described communication event did not actually
            occur.

        notDoneReason: Describes why the communication event did not occur in coded and/or textual
            form.

        category: The type of message conveyed such as alert, notification, reminder,
            instruction, etc.

        medium: A channel that was used for this communication (e.g. email, fax).

        subject: The patient or group that was the focus of this communication.

        recipient: The entity (e.g. person, organization, clinical information system, or device)
            which was the target of the communication. If receipts need to be tracked by
            individual, a separate resource instance will need to be created for each
            recipient.  Multiple recipient communications are intended where either a
            receipt(s) is not tracked (e.g. a mass mail-out) or is captured in aggregate
            (all emails confirmed received by a particular time).

        topic: The resources which were responsible for or related to producing this
            communication.

        context: The encounter within which the communication was sent.

        sent: The time when this communication was sent.

        received: The time when this communication arrived at the destination.

        sender: The entity (e.g. person, organization, clinical information system, or device)
            which was the source of the communication.

        reasonCode: The reason or justification for the communication.

        reasonReference: Indicates another resource whose existence justifies this communication.

        payload: Text, attachment(s), or resource(s) that was communicated to the recipient.

        note: Additional notes or commentary about the communication by the sender, receiver
            or other interested parties.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.communication_payload import (
            Communication_PayloadSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema

        if (
            max_recursion_limit
            and nesting_list.count("Communication") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Communication"]
        schema = StructType(
            [
                # This is a Communication resource
                StructField("resourceType", StringType(), True),
                # Identifiers associated with this Communication that are defined by business
                # processes and/ or used to refer to it when a direct URL reference to the
                # resource itself is not appropriate (e.g. in CDA documents, or in written /
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
                # A protocol, guideline, or other definition that was adhered to in whole or in
                # part by this communication event.
                StructField(
                    "definition",
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
                # An order, proposal or plan fulfilled in whole or in part by this
                # Communication.
                StructField(
                    "basedOn",
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
                # Part of this action.
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
                # The status of the transmission.
                StructField("status", StringType(), True),
                # If true, indicates that the described communication event did not actually
                # occur.
                StructField("notDone", BooleanType(), True),
                # Describes why the communication event did not occur in coded and/or textual
                # form.
                StructField(
                    "notDoneReason",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The type of message conveyed such as alert, notification, reminder,
                # instruction, etc.
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
                # A channel that was used for this communication (e.g. email, fax).
                StructField(
                    "medium",
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
                # The patient or group that was the focus of this communication.
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
                # The entity (e.g. person, organization, clinical information system, or device)
                # which was the target of the communication. If receipts need to be tracked by
                # individual, a separate resource instance will need to be created for each
                # recipient.  Multiple recipient communications are intended where either a
                # receipt(s) is not tracked (e.g. a mass mail-out) or is captured in aggregate
                # (all emails confirmed received by a particular time).
                StructField(
                    "recipient",
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
                # The resources which were responsible for or related to producing this
                # communication.
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
                # The encounter within which the communication was sent.
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
                # The time when this communication was sent.
                StructField("sent", StringType(), True),
                # The time when this communication arrived at the destination.
                StructField("received", StringType(), True),
                # The entity (e.g. person, organization, clinical information system, or device)
                # which was the source of the communication.
                StructField(
                    "sender",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The reason or justification for the communication.
                StructField(
                    "reasonCode",
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
                # Indicates another resource whose existence justifies this communication.
                StructField(
                    "reasonReference",
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
                # Text, attachment(s), or resource(s) that was communicated to the recipient.
                StructField(
                    "payload",
                    ArrayType(
                        Communication_PayloadSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Additional notes or commentary about the communication by the sender, receiver
                # or other interested parties.
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
