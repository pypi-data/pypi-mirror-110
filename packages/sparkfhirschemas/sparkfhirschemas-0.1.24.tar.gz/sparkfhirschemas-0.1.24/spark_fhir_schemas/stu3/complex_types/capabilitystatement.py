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
class CapabilityStatementSchema:
    """
    A Capability Statement documents a set of capabilities (behaviors) of a FHIR
    Server that may be used as a statement of actual server functionality or a
    statement of required or desired server implementation.
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
        A Capability Statement documents a set of capabilities (behaviors) of a FHIR
        Server that may be used as a statement of actual server functionality or a
        statement of required or desired server implementation.


        resourceType: This is a CapabilityStatement resource

        url: An absolute URI that is used to identify this capability statement when it is
            referenced in a specification, model, design or an instance. This SHALL be a
            URL, SHOULD be globally unique, and SHOULD be an address at which this
            capability statement is (or will be) published. The URL SHOULD include the
            major version of the capability statement. For more information see [Technical
            and Business Versions](resource.html#versions).

        version: The identifier that is used to identify this version of the capability
            statement when it is referenced in a specification, model, design or instance.
            This is an arbitrary value managed by the capability statement author and is
            not expected to be globally unique. For example, it might be a timestamp (e.g.
            yyyymmdd) if a managed version is not available. There is also no expectation
            that versions can be placed in a lexicographical sequence.

        name: A natural language name identifying the capability statement. This name should
            be usable as an identifier for the module by machine processing applications
            such as code generation.

        title: A short, descriptive, user-friendly title for the capability statement.

        status: The status of this capability statement. Enables tracking the life-cycle of
            the content.

        experimental: A boolean value to indicate that this capability statement is authored for
            testing purposes (or education/evaluation/marketing), and is not intended to
            be used for genuine usage.

        date: The date  (and optionally time) when the capability statement was published.
            The date must change if and when the business version changes and it must
            change if the status code changes. In addition, it should change when the
            substantive content of the capability statement changes.

        publisher: The name of the individual or organization that published the capability
            statement.

        contact: Contact details to assist a user in finding and communicating with the
            publisher.

        description: A free text natural language description of the capability statement from a
            consumer's perspective. Typically, this is used when the capability statement
            describes a desired rather than an actual solution, for example as a formal
            expression of requirements as part of an RFP.

        useContext: The content was developed with a focus and intent of supporting the contexts
            that are listed. These terms may be used to assist with indexing and searching
            for appropriate capability statement instances.

        jurisdiction: A legal or geographic region in which the capability statement is intended to
            be used.

        purpose: Explaination of why this capability statement is needed and why it has been
            designed as it has.

        copyright: A copyright statement relating to the capability statement and/or its
            contents. Copyright statements are generally legal restrictions on the use and
            publishing of the capability statement.

        kind: The way that this statement is intended to be used, to describe an actual
            running instance of software, a particular product (kind not instance of
            software) or a class of implementation (e.g. a desired purchase).

        instantiates: Reference to a canonical URL of another CapabilityStatement that this software
            implements or uses. This capability statement is a published API description
            that corresponds to a business service. The rest of the capability statement
            does not need to repeat the details of the referenced resource, but can do so.

        software: Software that is covered by this capability statement.  It is used when the
            capability statement describes the capabilities of a particular software
            version, independent of an installation.

        implementation: Identifies a specific implementation instance that is described by the
            capability statement - i.e. a particular installation, rather than the
            capabilities of a software program.

        fhirVersion: The version of the FHIR specification on which this capability statement is
            based.

        acceptUnknown: A code that indicates whether the application accepts unknown elements or
            extensions when reading resources.

        format: A list of the formats supported by this implementation using their content
            types.

        patchFormat: A list of the patch formats supported by this implementation using their
            content types.

        implementationGuide: A list of implementation guides that the server does (or should) support in
            their entirety.

        profile: A list of profiles that represent different use cases supported by the system.
            For a server, "supported by the system" means the system hosts/produces a set
            of resources that are conformant to a particular profile, and allows clients
            that use its services to search using this profile and to find appropriate
            data. For a client, it means the system will search by this profile and
            process data according to the guidance implicit in the profile. See further
            discussion in [Using Profiles](profiling.html#profile-uses).

        rest: A definition of the restful capabilities of the solution, if any.

        messaging: A description of the messaging capabilities of the solution.

        document: A document definition.

        """
        from spark_fhir_schemas.stu3.complex_types.contactdetail import (
            ContactDetailSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.usagecontext import (
            UsageContextSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.capabilitystatement_software import (
            CapabilityStatement_SoftwareSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.capabilitystatement_implementation import (
            CapabilityStatement_ImplementationSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.capabilitystatement_rest import (
            CapabilityStatement_RestSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.capabilitystatement_messaging import (
            CapabilityStatement_MessagingSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.capabilitystatement_document import (
            CapabilityStatement_DocumentSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("CapabilityStatement") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["CapabilityStatement"]
        schema = StructType(
            [
                # This is a CapabilityStatement resource
                StructField("resourceType", StringType(), True),
                # An absolute URI that is used to identify this capability statement when it is
                # referenced in a specification, model, design or an instance. This SHALL be a
                # URL, SHOULD be globally unique, and SHOULD be an address at which this
                # capability statement is (or will be) published. The URL SHOULD include the
                # major version of the capability statement. For more information see [Technical
                # and Business Versions](resource.html#versions).
                StructField("url", StringType(), True),
                # The identifier that is used to identify this version of the capability
                # statement when it is referenced in a specification, model, design or instance.
                # This is an arbitrary value managed by the capability statement author and is
                # not expected to be globally unique. For example, it might be a timestamp (e.g.
                # yyyymmdd) if a managed version is not available. There is also no expectation
                # that versions can be placed in a lexicographical sequence.
                StructField("version", StringType(), True),
                # A natural language name identifying the capability statement. This name should
                # be usable as an identifier for the module by machine processing applications
                # such as code generation.
                StructField("name", StringType(), True),
                # A short, descriptive, user-friendly title for the capability statement.
                StructField("title", StringType(), True),
                # The status of this capability statement. Enables tracking the life-cycle of
                # the content.
                StructField("status", StringType(), True),
                # A boolean value to indicate that this capability statement is authored for
                # testing purposes (or education/evaluation/marketing), and is not intended to
                # be used for genuine usage.
                StructField("experimental", BooleanType(), True),
                # The date  (and optionally time) when the capability statement was published.
                # The date must change if and when the business version changes and it must
                # change if the status code changes. In addition, it should change when the
                # substantive content of the capability statement changes.
                StructField("date", StringType(), True),
                # The name of the individual or organization that published the capability
                # statement.
                StructField("publisher", StringType(), True),
                # Contact details to assist a user in finding and communicating with the
                # publisher.
                StructField(
                    "contact",
                    ArrayType(
                        ContactDetailSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # A free text natural language description of the capability statement from a
                # consumer's perspective. Typically, this is used when the capability statement
                # describes a desired rather than an actual solution, for example as a formal
                # expression of requirements as part of an RFP.
                StructField("description", StringType(), True),
                # The content was developed with a focus and intent of supporting the contexts
                # that are listed. These terms may be used to assist with indexing and searching
                # for appropriate capability statement instances.
                StructField(
                    "useContext",
                    ArrayType(
                        UsageContextSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # A legal or geographic region in which the capability statement is intended to
                # be used.
                StructField(
                    "jurisdiction",
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
                # Explaination of why this capability statement is needed and why it has been
                # designed as it has.
                StructField("purpose", StringType(), True),
                # A copyright statement relating to the capability statement and/or its
                # contents. Copyright statements are generally legal restrictions on the use and
                # publishing of the capability statement.
                StructField("copyright", StringType(), True),
                # The way that this statement is intended to be used, to describe an actual
                # running instance of software, a particular product (kind not instance of
                # software) or a class of implementation (e.g. a desired purchase).
                StructField("kind", StringType(), True),
                # Reference to a canonical URL of another CapabilityStatement that this software
                # implements or uses. This capability statement is a published API description
                # that corresponds to a business service. The rest of the capability statement
                # does not need to repeat the details of the referenced resource, but can do so.
                # Software that is covered by this capability statement.  It is used when the
                # capability statement describes the capabilities of a particular software
                # version, independent of an installation.
                StructField(
                    "software",
                    CapabilityStatement_SoftwareSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Identifies a specific implementation instance that is described by the
                # capability statement - i.e. a particular installation, rather than the
                # capabilities of a software program.
                StructField(
                    "implementation",
                    CapabilityStatement_ImplementationSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The version of the FHIR specification on which this capability statement is
                # based.
                StructField("fhirVersion", StringType(), True),
                # A code that indicates whether the application accepts unknown elements or
                # extensions when reading resources.
                StructField("acceptUnknown", StringType(), True),
                # A list of the formats supported by this implementation using their content
                # types.
                # A list of the patch formats supported by this implementation using their
                # content types.
                # A list of implementation guides that the server does (or should) support in
                # their entirety.
                # A list of profiles that represent different use cases supported by the system.
                # For a server, "supported by the system" means the system hosts/produces a set
                # of resources that are conformant to a particular profile, and allows clients
                # that use its services to search using this profile and to find appropriate
                # data. For a client, it means the system will search by this profile and
                # process data according to the guidance implicit in the profile. See further
                # discussion in [Using Profiles](profiling.html#profile-uses).
                StructField(
                    "profile",
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
                # A definition of the restful capabilities of the solution, if any.
                StructField(
                    "rest",
                    ArrayType(
                        CapabilityStatement_RestSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # A description of the messaging capabilities of the solution.
                StructField(
                    "messaging",
                    ArrayType(
                        CapabilityStatement_MessagingSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # A document definition.
                StructField(
                    "document",
                    ArrayType(
                        CapabilityStatement_DocumentSchema.get_schema(
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
