from export import *



def print_imported_value(imported_value: str):
    try:
        print(imported_value)
    except:
        print(f"Failed to import: {imported_value}")


imported_values_list = [export_a, export_b, export_c, export_d]
for imported_value in imported_values_list:
    print_imported_value(imported_value)