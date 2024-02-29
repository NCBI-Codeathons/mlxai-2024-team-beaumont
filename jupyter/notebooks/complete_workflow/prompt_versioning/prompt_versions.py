import os
import re
    
def get_prompt(version_number=None):
    current_dir = os.path.dirname(__file__)
    prompt_dir = os.path.join(current_dir, "prompts")
    prompt_files = os.listdir(prompt_dir)
    
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}_[a-z]\d{2}\.txt")
    valid_files = [f for f in prompt_files if pattern.match(f)]
    
    valid_files.sort()
    
    if version_number:
        file_name = f"{version_number}.txt"
        file_path = os.path.join(prompt_dir, file_name)
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
        else:
            return "No prompt available for this version"
    
    newest_file = valid_files[-1] if valid_files else None
    if newest_file:
        with open(os.path.join(prompt_dir, newest_file), 'r') as file:
            return file.read()
    else:
        return "No prompts available"


# Example usage
version_number = "2028-02-28_a02"
prompt = get_prompt(version_number)
# prompt = get_prompt()
print(prompt)
