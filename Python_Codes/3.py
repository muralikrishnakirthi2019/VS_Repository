import ast
def find_path(dictionary, target_key, current_path=''):
    if isinstance(dictionary, dict):
        for key, value in dictionary.items():
            new_path = f"{current_path}.{key}" if current_path else key
            if key == target_key:
                return new_path
            elif isinstance(value, dict):
                result = find_path(value, target_key, new_path)
                if result:
                    return result
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    item_path = f"{new_path}[{index}]"
                    if isinstance(item, dict):
                        result = find_path(item, target_key, item_path)
                        if result:
                            return result
    return None
 
# Example dictionary
#example_dict = {
#    'a': {
#        'b': {
#            'c': 'd'
#        },
#        'e': 'f'
#    },
#    'g': [
#        {'h': 'i'},
#        {'j': 'k'}
#    ]
#}

with open('data.txt',  'r') as file:
    content = file.read()


example_dict = ast.literal_eval(content)

print(example_dict)




 
# Input: nested parameter name
parameter_name = input("Enter the nested parameter name: ")
 
# Find and print the path
path = find_path(example_dict, parameter_name)
if path:
    print(f"The path to '{parameter_name}' is: {path}")
else:
    print(f"'{parameter_name}' not found in the dictionary.")