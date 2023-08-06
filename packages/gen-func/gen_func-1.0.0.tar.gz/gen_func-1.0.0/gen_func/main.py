from prototype import (prompts, gpt_actions, meta_parsing)
import ast


# Variables that must first be established - user input and file path to meta schema
def generate_func(name, desc, tags, params, output, content, template, df_table_attr, df_table_def, df_file_def):
    """The master function that will generate the function body and total string length of
    all gpt requests and responses

    @param name: The name of the function.
    @param desc: The description of the function.
    @param tags: The list of tags associated with the function.
    @param params: The list of function parameters.
    @param output: The list of output values.
    @param content: The content of the function.
    @param template: The template string.
    @param df_table_attr: a df containing the table_attr info as a df, assumes that the columns
    'table_alias', 'attr_dbname', 'attr_desc', 'data_type', 'key_type' are present in the df
    @param df_table_def: a data frame containing the table_def info as a df, assumes the columns 'table_alias'
    and 'table_desc' are in the df
    @param df_file_def: a data frame containing the file_def info as a df, assumes the columns 'file_alias' and
    'file_desc' are in the df

    @return: a json containing the generated function body and the
    total string length of all prompts and responses to/from GPT
    """
    prompt_data = preprocessing(name, desc, tags, params, output, content, template,
                                df_table_attr, df_table_def, df_file_def)
    gpt_strings = gpt_calls(name, desc, tags, params, output, content, template, **prompt_data)
    processed_data = postprocessing(prompt_data['table_def_prompt'], prompt_data['file_def_prompt'], **gpt_strings)
    func = dict(body=processed_data['body'],
                total_string_length=processed_data['total_string_length'])
    return func


def preprocessing(name, desc, tags, params, output, content, template, df_table_attr, df_table_def, df_file_def):
    """The preprocessing function that reads the file containing the database schema
    (right now assumes an Excel sheet) and returns as a dict the prompts that will be fed to GPT to get
    a focused set of tables & files and the schema of tables including names, columns, column descriptions,
    data_type and is_key.

        @param name: The name of the function.
        @param desc: The description of the function.
        @param tags: The list of tags associated with the function.
        @param params: The list of function parameters.
        @param output: The list of output values.
        @param content: The content of the function.
        @param template: The template string.
        @param df_table_attr: a df containing the table_attr info as a df, assumes that the columns
        'table_alias', 'attr_dbname', 'attr_desc', 'data_type', 'key_type' are present in the df
        @param df_table_def: a data frame containing the table_def info as a df, assumes the columns 'table_alias'
        and 'table_desc' are in the df
        @param df_file_def: a data frame containing the file_def info as a df, assumes the columns 'file_alias' and
        'file_desc' are in the df

        @return: a json containing the generated table_def_prompt, file_def_prompt, and schema_table_attr
        """

    # parsing
    # Create table_attr_schema
    schema_table_attr = meta_parsing.get_table_attr_schema(df_table_attr)

    # Create table_def_schema
    schema_table_def = meta_parsing.get_table_def_schema(df_table_def)

    # Create file_def_schema
    schema_file_def = meta_parsing.get_file_def_schema(df_file_def)

    # Establish user input and create prompt for gpt to narrow down table_def_schema and file_def_schema
    table_def_prompt = prompts.get_tables_prompt(name, desc, tags, params, output, content, template, schema_table_def)
    file_def_prompt = prompts.get_files_prompt(name, desc, tags, params, output, content, template, schema_file_def)

    # Prepare response payload
    prompt_data = dict(
        table_def_prompt=table_def_prompt, file_def_prompt=file_def_prompt, schema_table_attr=schema_table_attr)
    return prompt_data


def gpt_calls(name, desc, tags, params, output, content, template,
              table_def_prompt, file_def_prompt, schema_table_attr):
    """The preprocessing function that reads the file containing the database schema
        (right now assumes an Excel sheet) and returns as a dict the prompts that will be fed to GPT to get
        a focused set of tables & files and the schema of tables including names, columns, column descriptions,
        data_type and is_key.

            @param name: The name of the function.
            @param desc: The description of the function.
            @param tags: The list of tags associated with the function.
            @param params: The list of function parameters.
            @param output: The list of output values.
            @param content: The content of the function.
            @param template: The template string.
            @param table_def_prompt: string containing the prompt for GPT to narrow down tables to a focused set
            @param file_def_prompt: string containing the prompt for GPT to narrow down files to a focused set
            @param schema_table_attr: schema of tables including names, columns, column descriptions,
            data_type and is_key.

            @return: a dict containing the generated GPT function, the prompt used to get the generated function,
            the focused set of tables and focused set of files
            """
    # Feed initial narrowing-down prompts to GPT and get the narrowed down schemas -> turn strings into dicts
    gpt_response_tables = gpt_actions.chatgpt_generate(table_def_prompt)
    narrow_table_def = ast.literal_eval(gpt_response_tables)
    gpt_response_files = gpt_actions.chatgpt_generate(file_def_prompt)
    narrow_file_def = ast.literal_eval(gpt_response_files)

    # Get a final_table_schema with necessary context using only tables in narrow_table_def
    final_tables_schema = meta_parsing.get_final_tables_schema(narrow_table_def, schema_table_attr)

    # Create function prompt using the now focused schemas
    function_prompt = prompts.get_function_prompt(name, desc, tags, params, output, content, template,
                                                  final_tables_schema, narrow_file_def)

    # Generate the function using gpt
    function = gpt_actions.chatgpt_generate(function_prompt)

    # return a dictionary
    gpt_strings = dict(function=function, function_prompt=function_prompt,
                       gpt_response_tables=gpt_response_tables, gpt_response_files=gpt_response_files)
    return gpt_strings


def postprocessing(table_def_prompt, file_def_prompt, function, function_prompt,
                   gpt_response_tables, gpt_response_files):
    """The postprocessing function that returns just the body of the
    generated GPT function and the total string length used for prompts and responses to/from GPT

    @param table_def_prompt: string containing the prompt for GPT to narrow down tables to a focused set
    @param file_def_prompt: string containing the prompt for GPT to narrow down files to a focused set
    @param function: the generated function from GPT
    @param function_prompt: the prompt used to get the generated function
    @param gpt_response_tables: the string rep. of the focused set of tables generated by GPT
    @param gpt_response_files: the string rep. of the focused set of files generated by GPT

    @return: a dict containing the body of the generated function and the total string length of all
    prompts and responses to/from GPT
    """
    body = parse_generated_function(function)
    total_string_length = get_gpt_string_length(table_def_prompt, file_def_prompt, function, function_prompt,
                                                gpt_response_tables, gpt_response_files)
    processed_data = dict(body=body, total_string_length=total_string_length)
    return processed_data


def parse_generated_function(function):
    """
    Given a Python function string, returns the body of the function
    between the colon and the return operator and includes the return operator line only when there
    is code on subsequent lines.

    @param function: The function generated by GPT to be parsed

    @ return: The body of the passed function
    """
    start_index = function.find(':\n') + 2
    return_index = function.rfind('return ')

    # Check if a return statement exists
    if return_index == -1:
        last_index = len(function)
    else:
        # Check if there is code after the last return statement
        for i in range(return_index+1, len(function)):
            if function[i] == '\n' and function[i+1] != '':
                break
            last_index = len(function)
        else: # no code after return statement (last line)
            last_index = return_index

    body = function[start_index:last_index]

    lines = body.split('\n')
    # Remove common indentation from all lines
    common_indent = min(len(line) - len(line.lstrip()) for line in lines)
    lines = [line[common_indent:] for line in lines]
    joined_lines = '\n'.join(lines)

    return joined_lines.rstrip('\n')


def get_gpt_string_length(table_def_prompt, file_def_prompt, function, function_prompt,
                          gpt_response_tables, gpt_response_files):
    """Given all the prompts made to GPT and responses generated by GPT returns total string length of all
    prompts and responses

        @param table_def_prompt: string containing the prompt for GPT to narrow down tables to a focused set
        @param file_def_prompt: string containing the prompt for GPT to narrow down files to a focused set
        @param function: the generated function from GPT
        @param function_prompt: the prompt used to get the generated function
        @param gpt_response_tables: the string rep. of the focused set of tables generated by GPT
        @param gpt_response_files: the string rep. of the focused set of files generated by GPT

        @return: a dict containing the body of the generated function and the total string length of all
        prompts and responses to/from GPT
        """
    string_list = [table_def_prompt, file_def_prompt, function_prompt,
                   function, gpt_response_tables, gpt_response_files]
    length = 0

    for string in string_list:
        length += len(string)

    return length
