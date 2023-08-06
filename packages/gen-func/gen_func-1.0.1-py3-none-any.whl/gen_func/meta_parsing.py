
def get_table_attr_schema(df_table_attr):
    """Returns the schema of the passed dataframe as a dictionary

    @param df_table_attr: is a dataframe from the meta DB
     containing the columns: table_alias, attr_dbname, attr_desc, data_type, and is_key

     @return: the schema as a dictionary"""

    # Create an empty dictionary to store the final result
    result_dict = {}

    # Iterate over the DataFrame rows
    for _, row in df_table_attr.iterrows():
        table_alias = row['table_alias']
        attr_dbname = row['attr_dbname']
        attr_desc = row['attr_desc']
        data_type = row['data_type']
        key_type = row['key_type']

        # Check if the table_alias exists in the result_dict, if not, add it with an empty definition
        if table_alias not in result_dict:
            result_dict[table_alias] = {'columns': [], 'desc': [], 'data_type': [], 'is_key': []}

        # Append the values to the corresponding keys in the dictionary
        result_dict[table_alias]['columns'].append(attr_dbname)
        result_dict[table_alias]['desc'].append(attr_desc)
        result_dict[table_alias]['data_type'].append(data_type)
        result_dict[table_alias]['is_key'].append(key_type == 'primary')

    return result_dict


def get_table_def_schema(df_table_def):
    """Returns the schema of the passed dataframe as a dictionary

    @param df_table_def: is a dataframe from the meta DB
     containing the columns: table_alias, 'table_desc'

    @return: the schema as a dictionary"""

    # Convert DataFrame columns to lists
    alias_list = df_table_def['table_alias'].tolist()
    desc_list = df_table_def['table_desc'].tolist()

    if len(alias_list) == 0:
        return {}
    else:
        # Create the dictionary
        result_dict = {
            'table_names': alias_list,
            'table_descriptions': desc_list
        }
        return result_dict


def get_file_def_schema(df_file_def):
    """Returns the schema of the passed dataframe as a dictionary

    @param df_file_def: is a dataframe from the meta DB
     containing the columns: file_alias, 'file_desc'

    @return: the schema as a dictionary"""

    # Convert DataFrame columns to lists
    alias_list = df_file_def['file_alias'].tolist()
    desc_list = df_file_def['file_desc'].tolist()

    if len(alias_list) == 0:
        return {}
    else:
        # Create the dictionary
        result_dict = {
            'file_names': alias_list,
            'file_descriptions': desc_list
        }
        return result_dict


def get_final_tables_schema(table_schema_generated, table_attr_schema):
    """Uses the GPT response to get_tables_prompt() and the result_dict from get_schema()
    to return a narrowed down result_dict for use in get_function_prompt

    @param table_schema_generated: a dict with only the tables and descriptions needed for the function generation
    @param table_attr_schema: the schema of the entire database to be accessed including columns and other info

    @return: the narrowed down schema as a dictionary"""

    result_dict = {}
    for table_name, table_data in table_attr_schema.items():
        if table_name in table_schema_generated['table_names']:
            aliases = table_schema_generated['table_names']
            aliases_index = aliases.index(table_name)
            table_alias = aliases[aliases_index]
            result_dict[table_alias] = {
                'columns': table_data['columns'],
                'desc': table_data['desc'],
                'data_type': table_data['data_type'],
                'is_key': table_data['is_key']
            }
    return result_dict

