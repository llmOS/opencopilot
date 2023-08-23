import os


def validate_system_prompt(file_path: str):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            prompt = f.read()
            if not "{question}" in prompt:
                raise Exception(f"'{{question}}' is missing in '{file_path}' prompt.")
            if not "{history}" in prompt:
                raise Exception(f"'{{history}}' is missing in '{file_path}' prompt.")
            if not "{context}" in prompt:
                raise Exception(f"'{{context}}' is missing in '{file_path}' prompt.")
    else:
        raise Exception(f"'{file_path}' is not a file path.")
