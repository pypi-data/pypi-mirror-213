import re


def validate_user_params(name, desc, tags, params, output, content, template):
    """Validate the user input parameters of a function.

        Checks the validity of the provided parameters for a function. Raises specific
        exceptions if any parameter fails the validation.

        @param name: The name of the function.
        @param desc: The description of the function.
        @param tags: The tags associated with the function.
        @param params: The parameters of the function.
        @param output: The output specifications of the function.
        @param content: The content of the function.
        @param template: The template used for the function.

        @raise TypeError: If any of the parameters have an invalid data type.
        @raise ValueError: If the name violates any naming conventions.

        @return: None
        """

    if not isinstance(name, str):
        raise TypeError('The name variable must be of type str.')
    if name[0].isdigit():
        raise ValueError("The function name cannot start with a number.")
    if re.search(r'\s', name):
        raise ValueError("The function name cannot contain whitespace.")
    if re.search(r'[^\w\s\d]', name):
        if not all(p == '_' for p in name):
            raise ValueError("The function name cannot contain punctuation except for underscores.")

    # Check type for params
    if params and (not isinstance(params, list) or not (len(params) > 0 and all(isinstance(p, dict) for p in params))):
        raise TypeError('The params variable must be of type List[Dict[str, Union[str, float, int, bool]]].')

    # Check type for desc
    if not isinstance(desc, str):
        raise TypeError('The desc variable must be of type str.')

    # Check type for tags
    if not isinstance(tags, list) or not (len(tags) > 0 and all(isinstance(t, str) for t in tags)):
        raise TypeError('The tags variable must be of type List[str].')

    # Check type for output
    if not isinstance(output, list) or not (len(output) > 0 and all(isinstance(out, dict) for out in output)):
        raise TypeError('The output variable must be of type List[Dict[str, Union[str, float, int, bool]]].')

    # Check type for content
    if content and not isinstance(content, str):
        raise TypeError('The content variable must be of type str or None.')

    # Check the type for template
    if not isinstance(template, str):
        raise TypeError('The template variable must be of type str.')


def validate_def_schema(schema):
    """Checks the validity of the tables_def_schema and the files_def_schema.

        @param schema: a dictionary containing table aliases and descriptions

        @raise TypeError: If any of the parameters have an invalid data type.

        @return: None
        """

    if schema and not isinstance(schema, dict):
        raise TypeError("Input must be a dictionary.")

    for value in schema.values():
        if not isinstance(value, list):
            raise TypeError("Dictionary values must be lists.")

        for item in value:
            if not isinstance(item, str):
                raise TypeError("List items must be strings.")


def validate_final_tables_schema(schema):
    """Checks the validity of the final_tables_schema .

            @param schema: a dictionary containing table aliases and descriptions

            @raise TypeError: If any of the parameters have an invalid data type.

            @return: None
            """

    if schema and not isinstance(schema, dict):
        raise TypeError("Invalid input: Expected a dictionary.")

    for value in schema.values():
        if not isinstance(value, dict):
            raise TypeError("Invalid input: Expected inner values to be dictionaries.")
        for inner_value in value.values():
            if not isinstance(inner_value, list):
                raise TypeError("Invalid input: Unexpected value type.")
            if isinstance(inner_value, list):
                for item in inner_value:
                    if (not isinstance(item, str)) and (not isinstance(item, bool)):
                        raise TypeError("Invalid input: Unexpected value type.")
    return True

