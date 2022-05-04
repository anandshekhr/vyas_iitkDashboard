import pandas as pd
import os

import pprint
input_folder = os.path.join(os.getcwd())
swl_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'swl_operation_components',header = None,skiprows = [0],engine="openpyxl")
ewl_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'ewl_operation_components',header = None,skiprows = [0],engine="openpyxl")
# rf_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'rf_operation_components',header = None,skiprows = [0],engine="openpyxl")
uf_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'uf_operation_components',header = None,skiprows = [0],engine="openpyxl")
rf_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'rf_operation_components',header = None,skiprows = [0],engine="openpyxl")
sh_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'sh_operation_components',header = None,skiprows = [0],engine="openpyxl")
# shell_op = pd.read_excel(os.path.join(input_folder,'inventory_data.xlsx'),sheet_name = 'sh_operation_components',header = None,skiprows = [0],engine="openpyxl")
operation_list = [rf_op,uf_op,swl_op,ewl_op,sh_op]
# operations = {}

components = {}

for items in operation_list:
    for index,row in items.iterrows():
        # if row not in components:
        components = {"Component Name":row[1],"Drawing No":row[2],"QPC":row[3],"Type":row[4],"Assembly Code":row[5],"Inventory":row[6]}
        print(components)
            




# for op in operation_list:
#     for index, row in op.iterrows():
#         # print(row[0],row[1],row[2],row[3],row[4])
#         if pd.isnull(row[0]):
#             continue
#         if row[0] not in operations:
#             operations[row[0]] = {}
#             operations[row[0]]["name"] = row[0]
#         if "inputs" not in operations[row[0]]:
#             operations[row[0]]["inputs"] = []
#         if "outputs" not in operations[row[0]]:
#             operations[row[0]]["outputs"] = []
#         if row[4] == "I":
#             ac = str(row[5])
#             if pd.isnull(row[5]):
#                 ac = "Z"
#             if ac != 0 and '=' in str(ac):
#                 index = ac.index("=")
#                 # ac = ac[index+1:]
#                 ac = ac[0:index]
            
#             operations[row[0]]["inputs"].append({
#                 "name": row[1],
#                 "part_no": 0 if pd.isnull(row[2]) else row[2],
#                 "qpc": row[3],
#                 "assembly_code": ac
#                 })
#         elif row[4] == "O":
#             ac = str(row[5])
#             if pd.isnull(row[5]):
#                 ac = "Z"
#             if ac != 0 and '=' in str(ac):
#                 index = ac.index("=")
#                 # ac = ac[index+1:]
#                 ac = ac[0:index]

#             operations[row[0]]["outputs"].append({
#                 "name": row[1],
#                 "part_no": 0 if pd.isnull(row[2]) else row[2],
#                 "qpc": row[3],
#                 "assembly_code": ac
#                 })

# pprint.pprint(operations)