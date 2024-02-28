import os
import re

def get_prompt(version_number):
    prompt_dir = "prompts"
    
    # List prompt files in the directory
    prompt_files = os.listdir(prompt_dir)
    
    # Filter prompt files matching the pattern
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}_[a-z]_\d{2}\.txt")
    valid_files = [f for f in prompt_files if pattern.match(f)]
    
    # Sort the valid files by date and version
    valid_files.sort()
    
    # Iterate through valid files to find the appropriate prompt
    for file_name in valid_files:
        with open(os.path.join(prompt_dir, file_name), 'r') as file:
            # Extract version number from the file name
            file_version = int(file_name.split('_')[-1].split('.')[0])
            if file_version >= version_number:
                return file.read()
    
    return "No prompt available for this version"

# Example usage
version_number = 5
prompt = get_prompt(version_number)
print(prompt)
