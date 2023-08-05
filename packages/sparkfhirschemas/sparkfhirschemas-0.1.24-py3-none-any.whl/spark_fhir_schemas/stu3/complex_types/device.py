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
class DeviceSchema:
    """
    This resource identifies an instance or a type of a manufactured item that is
    used in the provision of healthcare without being substantially changed
    through that activity. The device may be a medical or non-medical device.
    Medical devices include durable (reusable) medical equipment, implantable
    devices, as well as disposable equipment used for diagnostic, treatment, and
    research for healthcare and public health.  Non-medical devices may include
    items such as a machine, cellphone, computer, application, etc.
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
        This resource identifies an instance or a type of a manufactured item that is
        used in the provision of healthcare without being substantially changed
        through that activity. The device may be a medical or non-medical device.
        Medical devices include durable (reusable) medical equipment, implantable
        devices, as well as disposable equipment used for diagnostic, treatment, and
        research for healthcare and public health.  Non-medical devices may include
        items such as a machine, cellphone, computer, application, etc.


        resourceType: This is a Device resource

        identifier: Unique instance identifiers assigned to a device by manufacturers other
            organizations or owners.

        udi: [Unique device identifier (UDI)](device.html#5.11.3.2.2) assigned to device
            label or package.

        status: Status of the Device availability.

        type: Code or identifier to identify a kind of device.

        lotNumber: Lot number assigned by the manufacturer.

        manufacturer: A name of the manufacturer.

        manufactureDate: The date and time when the device was manufactured.

        expirationDate: The date and time beyond which this device is no longer valid or should not be
            used (if applicable).

        model: The "model" is an identifier assigned by the manufacturer to identify the
            product by its type. This number is shared by the all devices sold as the same
            type.

        version: The version of the device, if the device has multiple releases under the same
            model, or if the device is software or carries firmware.

        patient: Patient information, If the device is affixed to a person.

        owner: An organization that is responsible for the provision and ongoing maintenance
            of the device.

        contact: Contact details for an organization or a particular human that is responsible
            for the device.

        location: The place where the device can be found.

        url: A network address on which the device may be contacted directly.

        note: Descriptive information, usage information or implantation information that is
            not captured in an existing element.

        safety: Provides additional safety characteristics about a medical device.  For
            example devices containing latex.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.device_udi import Device_UdiSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.contactpoint import (
            ContactPointSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.annotation import AnnotationSchema

        if (
            max_recursion_limit and nesting_list.count("Device") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Device"]
        schema = StructType(
            [
                # This is a Device resource
                StructField("resourceType", StringType(), True),
                # Unique instance identifiers assigned to a device by manufacturers other
                # organizations or owners.
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
                # [Unique device identifier (UDI)](device.html#5.11.3.2.2) assigned to device
                # label or package.
                StructField(
                    "udi",
                    Device_UdiSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Status of the Device availability.
                StructField("status", StringType(), True),
                # Code or identifier to identify a kind of device.
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
                # Lot number assigned by the manufacturer.
                StructField("lotNumber", StringType(), True),
                # A name of the manufacturer.
                StructField("manufacturer", StringType(), True),
                # The date and time when the device was manufactured.
                StructField("manufactureDate", StringType(), True),
                # The date and time beyond which this device is no longer valid or should not be
                # used (if applicable).
                StructField("expirationDate", StringType(), True),
                # The "model" is an identifier assigned by the manufacturer to identify the
                # product by its type. This number is shared by the all devices sold as the same
                # type.
                StructField("model", StringType(), True),
                # The version of the device, if the device has multiple releases under the same
                # model, or if the device is software or carries firmware.
                StructField("version", StringType(), True),
                # Patient information, If the device is affixed to a person.
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
                # An organization that is responsible for the provision and ongoing maintenance
                # of the device.
                StructField(
                    "owner",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Contact details for an organization or a particular human that is responsible
                # for the device.
                StructField(
                    "contact",
                    ArrayType(
                        ContactPointSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # The place where the device can be found.
                StructField(
                    "location",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # A network address on which the device may be contacted directly.
                StructField("url", StringType(), True),
                # Descriptive information, usage information or implantation information that is
                # not captured in an existing element.
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
                # Provides additional safety characteristics about a medical device.  For
                # example devices containing latex.
                StructField(
                    "safety",
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
