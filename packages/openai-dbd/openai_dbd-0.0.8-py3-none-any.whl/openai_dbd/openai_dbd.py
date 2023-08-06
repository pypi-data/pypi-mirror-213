import string, random, os, requests
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side

def callOpenAI(URL, HEADERS, MY_PROMPT):
    OpenAIData = requests.post(URL, headers = HEADERS, json = {
        "model": 'gpt-3.5-turbo',
        "messages": [
            {
            "role": "user",
            "content": MY_PROMPT
            }
        ],
        "temperature": 0.7
    })

    return OpenAIData.json()

def giveRandName(l = 7):
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=l))
    return str(res)

def sql_prompt(projectCategory, featureOfDBStructure, open_ai_data):
    promptX = f"""
    Generate SQL Queries for *{projectCategory}* that provides features like
    `{featureOfDBStructure}`

    Maintain proper relations between these tables and provide information for each table. 
    Additionally, normalize the tables for better understanding and performance, and add an 'id' field with 'auto_increment' to each table.
    Add created_at and updated_at fields to each table.
    Place all root tables at the top, as other tables depend on them.
    I want table_name, column_name, data_type, size and constraint.
    In the constraint column, capitalize all letters except for the table names.
    Keep tables name small everywhere
    Keep in mind that dont use keywords that are researved for mysql

    I want you to only reply the sql command and nothing else, do not write explanations and any starting and ending sentences follow my instructions strictly.
    """

    return callOpenAI(open_ai_data['url'], open_ai_data['headers'], promptX)

def json_prompt(projectCategory, featureOfDBStructure, open_ai_data):
    promptX = """
    Generate Database Architecture for """ + projectCategory + """ that provides features like
    """ + featureOfDBStructure + """
    Maintain proper relations between these tables and provide information for each table. Additionally, normalize the tables for better understanding and performance, and add an 'id' field with 'auto_increment' to each table.
    Add created_at and updated_at fields to each table.
    Place all root tables at the top, as other tables depend on them.
    I want table_name, column_name, data_type, size and constraint.
    In the constraint column, capitalize all letters except for the table names.
    Keep in mind that dont use keywords that are researved for mysql

    `Do not include any explanations and extra content`, only provide formatted JSON response

    Json response example
    [{
        "table_name": "Table Name",
        "columns": [{"column_name": "Col Name", "data_type": "int", "size": "15", "constraint": "constraints"}, {"column_name": "Col Name", "data_type": "int", "size": "15", "constraint": "constraints"}]
    },
    {
        "table_name": "Table Name",
        "columns": [{"column_name": "Col Name", "data_type": "int", "size": "15", "constraint": "constraints"}, {"column_name": "Col Name", "data_type": "int", "size": "15", "constraint": "constraints"}]
    }]
    """

    return callOpenAI(open_ai_data['url'], open_ai_data['headers'], promptX)

def correct_schema(sql_schema, open_ai_data):
    promptX = f"""
    I want you to act as SQL parser. 
    I will give you instructions and you will only reply me with SQl query.

    I have an existing database schema that I want you to review.
    I would like you to correct any issues with the schema and redesign whole schema including create statments. 
    Additionally, if the schema is not normalized, please normalize it.
    Also, modify the current schema if it has performance issues.
    Also, don't add any sql comments in result.
    Also, if tables dosn't have created_at and updated_at columns, add it.
    Please keep in mind every table i provide you in schema should be there and modified if required, 
    Place all root tables at the top, as other tables depend on them
    Here is my current schema.
    `{sql_schema}`

    I want you to only reply the sql queries and nothing else, 
    do not write explanations and any starting and ending sentences follow my instructions strictly.
    """

    return callOpenAI(open_ai_data['url'], open_ai_data['headers'], promptX)

def generate_sql(db_name, data):
    fName = giveRandName(10)
    with open(f"{fName}.sql", 'w') as file:
        dbName = db_name.replace(' ', '_').replace('-', '_').lower()
        file.write(f"CREATE DATABASE {dbName};\n\n")
        file.write(f"USE {dbName};\n\n")
        file.write(data)

    response = HttpResponse(open(f'{fName}.sql', 'rb'))
    response['Content-Disposition'] = f'attachment; filename={fName}.sql'
    os.remove(f'{fName}.sql')
    return response

def generate_excel(file_name, json_data):
    wb = Workbook()
    sheet = wb.active

    bold_font = Font(bold=True)
    table_name_font = Font(bold=True, size=16)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    column_widths = {
        "column_name": 0.20,
        "data_type": 0.15,
        "size": 0.1,
        "constraint": 0.45
    }

    for index, table in enumerate(json_data):
        table_start_row = sheet.max_row + 1
        table_end_row = table_start_row + 1
        sheet.merge_cells(start_row=table_start_row, start_column=3, end_row=table_end_row, end_column=6)
        cell = sheet.cell(row=table_start_row, column=3, value=f"{index + 1}. {table['table_name']}")
        cell.font = table_name_font
        # cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.alignment = Alignment(vertical="center")

        headers = ["column_name", "data_type", "size", "constraint"]
        sheet.append([""] * 2 + [header.upper() for header in headers])

        sheet.append([""] * 2 + [header.upper() for header in headers])
        for col, header in enumerate(sheet[sheet.max_row], start=3):
            header.font = bold_font

        for column in table["columns"]:
            column_name = column["column_name"]
            data_type = column["data_type"].upper()
            size = column["size"]
            constraint = column["constraint"]

            sheet.append([""] * 2 + [column_name, data_type, size, constraint])
        sheet.append([""] * 6 )
        
        table_start_cell = sheet.cell(row=table_start_row, column=3)
        table_end_cell = sheet.cell(row=sheet.max_row, column=6)
        table_range = table_start_cell.coordinate + ':' + table_end_cell.coordinate
        for row in sheet[table_range]:
            for cell in row:
                cell.border = thin_border
                
        for col in range(3, sheet.max_column + 1):
            column_name = sheet.cell(row=table_start_row + 1, column=col).value
            width = column_widths.get(column_name.lower(), 1)
            sheet.column_dimensions[chr(col + 64)].width = width * 100
            
        sheet.append([])
        empty_row = sheet.max_row
        for col in range(1, sheet.max_column + 1):
            sheet.cell(row=empty_row, column=col).border = None

    fName = giveRandName(10)
    file_name = file_name.replace(' ', '_').replace('-', '_').lower()
    wb.save(f'{fName}.xlsx')
    response = HttpResponse(open(f'{fName}.xlsx', 'rb'))
    response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
    os.remove(f'{fName}.xlsx')
    return response