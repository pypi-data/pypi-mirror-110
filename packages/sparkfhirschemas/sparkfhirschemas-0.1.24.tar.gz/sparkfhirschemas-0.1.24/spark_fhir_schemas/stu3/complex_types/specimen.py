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
class SpecimenSchema:
    """
    A sample to be used for analysis.
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
        A sample to be used for analysis.


        resourceType: This is a Specimen resource

        identifier: Id for specimen.

        accessionIdentifier: The identifier assigned by the lab when accessioning specimen(s). This is not
            necessarily the same as the specimen identifier, depending on local lab
            procedures.

        status: The availability of the specimen.

        type: The kind of material that forms the specimen.

        subject: Where the specimen came from. This may be from the patient(s) or from the
            environment or a device.

        receivedTime: Time when specimen was received for processing or testing.

        parent: Reference to the parent (source) specimen which is used when the specimen was
            either derived from or a component of another specimen.

        request: Details concerning a test or procedure request that required a specimen to be
            collected.

        collection: Details concerning the specimen collection.

        processing: Details concerning processing and processing steps for the specimen.

        container: The container holding the specimen.  The recursive nature of containers; i.e.
            blood in tube in tray in rack is not addressed here.

        note: To communicate any details or issues about the specimen or during the specimen
            collection. (for example: broken vial, sent with patient, frozen).

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.specimen_collection import (
            Specimen_CollectionSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.specimen_processing import (
            Specimen_ProcessingSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.specimen_container import (
            Specimen_ContainerSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema

        if (
            max_recursion_limit
            and nesting_list.count("Specimen") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Specimen"]
        schema = StructType(
            [
                # This is a Specimen resource
                StructField("resourceType", StringType(), True),
                # Id for specimen.
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
                # The identifier assigned by the lab when accessioning specimen(s). This is not
                # necessarily the same as the specimen identifier, depending on local lab
                # procedures.
                StructField(
                    "accessionIdentifier",
                    IdentifierSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The availability of the specimen.
                StructField("status", StringType(), True),
                # The kind of material that forms the specimen.
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
                # Where the specimen came from. This may be from the patient(s) or from the
                # environment or a device.
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
                # Time when specimen was received for processing or testing.
                StructField("receivedTime", StringType(), True),
                # Reference to the parent (source) specimen which is used when the specimen was
                # either derived from or a component of another specimen.
                StructField(
                    "parent",
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
                # Details concerning a test or procedure request that required a specimen to be
                # collected.
                StructField(
                    "request",
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
                # Details concerning the specimen collection.
                StructField(
                    "collection",
                    Specimen_CollectionSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Details concerning processing and processing steps for the specimen.
                StructField(
                    "processing",
                    ArrayType(
                        Specimen_ProcessingSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # The container holding the specimen.  The recursive nature of containers; i.e.
                # blood in tube in tray in rack is not addressed here.
                StructField(
                    "container",
                    ArrayType(
                        Specimen_ContainerSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # To communicate any details or issues about the specimen or during the specimen
                # collection. (for example: broken vial, sent with patient, frozen).
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
