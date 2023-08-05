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
class ValueSetSchema:
    """
    A value set specifies a set of codes drawn from one or more code systems.
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
        A value set specifies a set of codes drawn from one or more code systems.


        resourceType: This is a ValueSet resource

        url: An absolute URI that is used to identify this value set when it is referenced
            in a specification, model, design or an instance. This SHALL be a URL, SHOULD
            be globally unique, and SHOULD be an address at which this value set is (or
            will be) published. The URL SHOULD include the major version of the value set.
            For more information see [Technical and Business
            Versions](resource.html#versions).

        identifier: A formal identifier that is used to identify this value set when it is
            represented in other formats, or referenced in a specification, model, design
            or an instance.

        version: The identifier that is used to identify this version of the value set when it
            is referenced in a specification, model, design or instance. This is an
            arbitrary value managed by the value set author and is not expected to be
            globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a
            managed version is not available. There is also no expectation that versions
            can be placed in a lexicographical sequence.

        name: A natural language name identifying the value set. This name should be usable
            as an identifier for the module by machine processing applications such as
            code generation.

        title: A short, descriptive, user-friendly title for the value set.

        status: The status of this value set. Enables tracking the life-cycle of the content.

        experimental: A boolean value to indicate that this value set is authored for testing
            purposes (or education/evaluation/marketing), and is not intended to be used
            for genuine usage.

        date: The date  (and optionally time) when the value set was published. The date
            must change if and when the business version changes and it must change if the
            status code changes. In addition, it should change when the substantive
            content of the value set changes. (e.g. the 'content logical definition').

        publisher: The name of the individual or organization that published the value set.

        contact: Contact details to assist a user in finding and communicating with the
            publisher.

        description: A free text natural language description of the value set from a consumer's
            perspective.

        useContext: The content was developed with a focus and intent of supporting the contexts
            that are listed. These terms may be used to assist with indexing and searching
            for appropriate value set instances.

        jurisdiction: A legal or geographic region in which the value set is intended to be used.

        immutable: If this is set to 'true', then no new versions of the content logical
            definition can be created.  Note: Other metadata might still change.

        purpose: Explaination of why this value set is needed and why it has been designed as
            it has.

        copyright: A copyright statement relating to the value set and/or its contents. Copyright
            statements are generally legal restrictions on the use and publishing of the
            value set.

        extensible: Whether this is intended to be used with an extensible binding or not.

        compose: A set of criteria that define the content logical definition of the value set
            by including or excluding codes from outside this value set. This I also known
            as the "Content Logical Definition" (CLD).

        expansion: A value set can also be "expanded", where the value set is turned into a
            simple collection of enumerated codes. This element holds the expansion, if it
            has been performed.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.contactdetail import (
            ContactDetailSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.usagecontext import (
            UsageContextSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import (
            CodeableConceptSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.valueset_compose import (
            ValueSet_ComposeSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.valueset_expansion import (
            ValueSet_ExpansionSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("ValueSet") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ValueSet"]
        schema = StructType(
            [
                # This is a ValueSet resource
                StructField("resourceType", StringType(), True),
                # An absolute URI that is used to identify this value set when it is referenced
                # in a specification, model, design or an instance. This SHALL be a URL, SHOULD
                # be globally unique, and SHOULD be an address at which this value set is (or
                # will be) published. The URL SHOULD include the major version of the value set.
                # For more information see [Technical and Business
                # Versions](resource.html#versions).
                StructField("url", StringType(), True),
                # A formal identifier that is used to identify this value set when it is
                # represented in other formats, or referenced in a specification, model, design
                # or an instance.
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
                # The identifier that is used to identify this version of the value set when it
                # is referenced in a specification, model, design or instance. This is an
                # arbitrary value managed by the value set author and is not expected to be
                # globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a
                # managed version is not available. There is also no expectation that versions
                # can be placed in a lexicographical sequence.
                StructField("version", StringType(), True),
                # A natural language name identifying the value set. This name should be usable
                # as an identifier for the module by machine processing applications such as
                # code generation.
                StructField("name", StringType(), True),
                # A short, descriptive, user-friendly title for the value set.
                StructField("title", StringType(), True),
                # The status of this value set. Enables tracking the life-cycle of the content.
                StructField("status", StringType(), True),
                # A boolean value to indicate that this value set is authored for testing
                # purposes (or education/evaluation/marketing), and is not intended to be used
                # for genuine usage.
                StructField("experimental", BooleanType(), True),
                # The date  (and optionally time) when the value set was published. The date
                # must change if and when the business version changes and it must change if the
                # status code changes. In addition, it should change when the substantive
                # content of the value set changes. (e.g. the 'content logical definition').
                StructField("date", StringType(), True),
                # The name of the individual or organization that published the value set.
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
                # A free text natural language description of the value set from a consumer's
                # perspective.
                StructField("description", StringType(), True),
                # The content was developed with a focus and intent of supporting the contexts
                # that are listed. These terms may be used to assist with indexing and searching
                # for appropriate value set instances.
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
                # A legal or geographic region in which the value set is intended to be used.
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
                # If this is set to 'true', then no new versions of the content logical
                # definition can be created.  Note: Other metadata might still change.
                StructField("immutable", BooleanType(), True),
                # Explaination of why this value set is needed and why it has been designed as
                # it has.
                StructField("purpose", StringType(), True),
                # A copyright statement relating to the value set and/or its contents. Copyright
                # statements are generally legal restrictions on the use and publishing of the
                # value set.
                StructField("copyright", StringType(), True),
                # Whether this is intended to be used with an extensible binding or not.
                StructField("extensible", BooleanType(), True),
                # A set of criteria that define the content logical definition of the value set
                # by including or excluding codes from outside this value set. This I also known
                # as the "Content Logical Definition" (CLD).
                StructField(
                    "compose",
                    ValueSet_ComposeSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # A value set can also be "expanded", where the value set is turned into a
                # simple collection of enumerated codes. This element holds the expansion, if it
                # has been performed.
                StructField(
                    "expansion",
                    ValueSet_ExpansionSchema.get_schema(
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
