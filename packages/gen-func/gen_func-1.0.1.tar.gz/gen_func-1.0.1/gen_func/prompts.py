from gen_func import validation


def get_tables_prompt(name, desc, tags, params, output, content, template, table_def_schema):
    """Based on user input and the db schema, creates a request for gpt to narrow
    down the tables_def_schema dictionary to only the necessary tables

    @param name: The name of the function.
    @param desc: The description of the function.
    @param tags: The list of tags associated with the function.
    @param params: The list of function parameters.
    @param output: The list of output values.
    @param content: The content of the function.
    @param template: The template string.
    @param table_def_schema: A dictionary of database table names and descriptions

    @return: The prompt to be fed to GPT"""

    # Validate that the parameters taken as input are of the correct type/value
    validation.validate_user_params(name, desc, tags, params, output, content, template)
    validation.validate_def_schema(table_def_schema)

    if table_def_schema:
        request = "If a python function is to be created with the following properties, return " \
                  "a narrowed down version of this dictionary " \
                  f"{table_def_schema} to only include the tables necessary for the function:\n" \
                  f"Function name = {name}\n" \
                  f"Function description = {desc}\n" \
                  f"Function tags = {tags}\n" \
                  f"Function input parameter names with corresponding data types and defaults = {params}\n" \
                  f"Function output (what is returned) = {output}\n" \
                  f"Code template = {template}\n" \
                  "If no tables are necessary for the operation, return '{}' as your text response. " \
                  "Only respond with a dictionary and no additional text/descriptions."
    else:
        request = "return '{}' as your response to this prompt"

    return request


def get_files_prompt(name, desc, tags, params, output, content, template, file_def_schema):
    """Based on user input and the db schema, creates a request for gpt to narrow
        down the files_schema dictionary to only the necessary files

        @param name: The name of the function.
        @param desc: The description of the function.
        @param tags: The list of tags associated with the function.
        @param params: The list of function parameters.
        @param output: The list of output values.
        @param content: The content of the function.
        @param template: The template string.
        @param file_def_schema: A dictionary of database file names and descriptions

        @return: The prompt to be fed to GPT"""

    # Validate that the parameters taken as input are of the correct type/value
    validation.validate_user_params(name, desc, tags, params, output, content, template)
    validation.validate_def_schema(file_def_schema)

    if file_def_schema:
        request = "If a python function is to be created with the following properties, return " \
                  "a narrowed down version of this dictionary " \
                  f"{file_def_schema} to only include the files necessary for the function:\n" \
                  f"Function name = {name}\n" \
                  f"Function description = {desc}\n" \
                  f"Function tags = {tags}\n" \
                  f"Function input parameter names with corresponding data types and defaults = {params}\n" \
                  f"Function output (what is returned) = {output}\n" \
                  f"Code template = {template}\n" \
                  "If no files are necessary for the operation, return '{}' as your text response. " \
                  "Only respond with a dictionary and no additional text/descriptions."
    else:
        request = "return '{}' as your response to this prompt"

    return request


def get_function_prompt(name, desc, tags, params, output, content, template, final_tables_schema, file_def_schema):
    """Based on user input and the db schema, creates a request for gpt to narrow
            down the files_schema dictionary to only the necessary files

            @param name: The name of the function.
            @param desc: The description of the function.
            @param tags: The list of tags associated with the function.
            @param params: The list of function parameters.
            @param output: The list of output values.
            @param content: The content of the function.
            @param template: The template string.
            @param final_tables_schema: A narrowed down dictionary of database table names and descriptions
            @param file_def_schema: A dictionary of database file names and descriptions

            @return: The prompt to be fed to GPT"""

    # Validate that the parameters taken as input are of the correct type/value
    validation.validate_user_params(name, desc, tags, params, output, content, template)
    validation.validate_final_tables_schema(final_tables_schema)
    validation.validate_def_schema(file_def_schema)

    # String manipulation for create/update cases
    if content:
        action = "Optimize"
        action2 = "but keep"
        update_body = f"7.Code to Update = {content}\n"
    else:
        action = "Create"
        action2 = "with"
        update_body = ""

    if final_tables_schema:
        tables_context = "The `Table` class wraps an ORM and contains a `read_data` method and " \
          "`create_data`, `update_data`, and `delete_data` methods." \
          "All methods in the `Table` class return pandas Dataframes. " \
          "The `Table` `read_data` method must take parameters as follows:" \
          " `read_data(columns=[], where={'*__postfix': some_variable})`. " \
          "The `*` should be replaced with and represent a column or other variable. " \
          "The postfix operators can be any " \
          "of the following as they are shown with their equivalent SQL operator-\n" \
          "eq: =\n" \
          "in: IN\n" \
          "gte: >=\n" \
          "gt: >\n" \
          "lte: <=\n" \
          "lt: <\n" \
          "neq: !=\n" \
          "nin: NOT IN\n" \
          "Ensure `*` and `some_variable` are of the same data type. " \
          "The `create_data`, `update_data`, and `delete_data` methods take as input a variable which is a " \
          "DataFrame with some columns representing a composite primary key or a column representing a primary " \
          "key, and the additional columns representing data. For example, calling the `update_data` method " \
          "may look similar to `component.table['table_alias'].update_data(df_name)`. Calling the `create_data method " \
          "may look similar to `component.table['table_alias'].create_data(df_name)`. Calling the 'delete_data method " \
          "may look similar to ``component.table['table_alias'].delete_data(df_name)`." \
          "For the `create_data` method, if primary key in the passed df do not " \
          "already exist in the table, these records should be created in the table. " \
          "For the `update_data` method, if keys in the passed df exist in the table, these records should " \
          "be updated in the table. For the `delete` method, if keys in the passed df exist in the table, " \
          "these records should be deleted.\n"\
          "The following dictionary shows the schema of the database tables which the function is able to " \
          f"access through the component variable: {final_tables_schema}.\n" \
          "The schema provided is in the format: {'table_name': " \
          "{'columns': ['column1', 'column2',...], {'desc': ['column 1 desc', 'column 2 desc',...], 'data_type': " \
          "['column1 data type', 'column2 data type'...], 'is_key': [True, False,...]}, ...}." \
          "Note that if multiple columns in the same table are marked as 'True' for 'is_key', " \
          "this table has a composite key.\n" \
          "To query certain data from a table, you may need to use data from a different table related " \
          "through an attribute which is like a foreign key. Only use primary keys and 'foreign keys' to access " \
          "specific records in a table." \
          "These related columns will have the same data and same data type.\n"
    else:
        tables_context = ""

    if file_def_schema:
        files_context = "The File class may contain a read_data method and write_data method which return byte objects." \
              "Ensure optimal code for file reading and writing " \
              "in terms of space and time complexity by using generators." \
              "Generator syntax may look similar to `generator = component.file[file_alias].read_binary()`. " \
              "The `write_data` function takes a generator as input." \
              "Assume utf-8 as default encoding. \n" \
              "The following dictionary shows the files within the database which the function is able to access " \
              f"through the component variable: {file_def_schema}.\n"
    else:
        files_context = ""

    if final_tables_schema or file_def_schema:
        context = "\nKeep `component` and `payload` as parameters of the function " \
                  "along with the other Function parameters.\n" \
                  "Note that the variable `component = Component()`.\n" \
                  "The `Component` class may contain:\n" \
                  "- an instance variable `table` which is a dict of table name mapped to `Table` object.\n" \
                  "- an instance variable `file` which is a dict of file name mapped to `File` object.\n" \
                  "The `Component` class may be structured:\n" \
                  "```class Component():\n" \
                  "\tdef __init__(self):\n" \
                  "\t\tself.tables = {}\n" \
                  "\t\tself.files = {}```\n" \
                  f"{tables_context}" \
                  f"{files_context}" \
                  "Payload is a variable that describes the metadata " \
                  "that comes from a request. Be sure to use component and payload in the function as needed when the " \
                  "Function description describes a database action to be performed.\n" \
                  "Do not query using SQL syntax. " \
                  "Always name dataframes with 'df_' prefix. " \
                  "Ensure optimal code using pandas library and numpy vectorization."
    else:
        context = ""
    # prepare a prompt for a new code from Chat GPT using the input parameters
    # Descriptions of Component and Payload may need adjustment
    request = f"{action} a python function {action2} the following properties:\n" \
              f"1.Function name = {name}\n" \
              f"2.Function description = {desc}\n" \
              f"3.Function tags = {tags}\n" \
              f"4.Function input parameter names with corresponding data types and defaults = {params}\n" \
              f"5.Function output (what is returned) = {output}\n" \
              f"6.Code template = {template}\n" \
              f"{update_body}" \
              "Return no descriptions. " \
              "Return valid syntax. " \
              "Include nothing before the function definition. " \
              "Return only the function." \
              f"{context}"
    return request

