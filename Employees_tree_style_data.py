import pandas as pd
from collections import defaultdict
import json

# Provide Path of employee dataset Excel file here
excel_file_path = "EmployeesData.xlsx"


# DFS Implementation
def build_employee_tree(employee_id, employees_adjacency_list, employees_data):
    employee_info = {
        'employeeID': employee_id,
        'name': employees_data[employee_id]['name']
    }
    reportees = [build_employee_tree(reportee_id, employees_adjacency_list, employees_data) for reportee_id in
                 employees_adjacency_list[employee_id]]
    if reportees:
        employee_info['reportees'] = reportees
    return employee_info


def employee_tabular_to_json():
    dataframes = pd.read_excel(excel_file_path)  # Reading Employees data excel file using Pandas
    employees_adjacency_list = defaultdict(list)  # Graph(adjacency list) to represent relations between employees
    employees_data = {}  # Dictionary for O(1) lookup of employee data ex- employee Name, department using employee ID

    # Creating employees_adjacency_list and adding data in employee_data dictionary
    for _, row in dataframes.iterrows():
        employee_id = row["EMPLOYEE_ID"]
        manager_id = row["MANAGER EMPLOYEE_ID"]
        employee_name = row["NAME"]
        employees_data[employee_id] = {'name': employee_name}
        if pd.notna(manager_id):
            employees_adjacency_list[manager_id].append(employee_id)

    # Finding Root employee for graph
    root_employee_id = dataframes[dataframes["MANAGER EMPLOYEE_ID"].isnull()]["EMPLOYEE_ID"].iloc[0]

    # DFS(Running Depth First Search for graph Traversal)
    employee_tree = build_employee_tree(root_employee_id, employees_adjacency_list, employees_data)

    # Print Employees tree as JSON
    employee_tree_json = json.dumps(employee_tree, indent=4)
    return employee_tree_json


print(employee_tabular_to_json())

# Time Complexity - O(N) where N = Number of employees
