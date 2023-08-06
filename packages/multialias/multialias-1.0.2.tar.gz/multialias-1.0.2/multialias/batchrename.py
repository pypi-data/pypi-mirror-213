import os
import subprocess
import tempfile
import sys

def get_default_text_editor():
    if os.name == 'posix':  # Unix/Linux/MacOS
        return os.environ.get('EDITOR', 'vi')
    elif os.name == 'nt':  # Windows
        return os.environ.get('EDITOR', 'notepad')

def get_available_text_editors():
    if os.name == 'posix':  # Unix/Linux/MacOS
        return ['vi', 'emacs', 'nano']
    elif os.name == 'nt':  # Windows
        return ['notepad', 'notepad++', 'sublime_text']

def batch_rename(directory, text_editor=None):
    # Get the list of files in the specified directory
    file_list = os.listdir(directory)
    
    # Create a temporary file to hold the filenames
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
    try:
        # Write the filenames to the temporary file
        for filename in file_list:
            temp_file.write(filename + '\n')
        
        # Close the temporary file
        temp_file.close()
        
        # Determine the text editor to use
        if text_editor is None:
            text_editor = get_default_text_editor()
        
        # Open the temporary file in the text editor
        subprocess.call([text_editor, temp_file.name])
        
        # Read the modified filenames from the temporary file
        with open(temp_file.name, 'r') as f:
            modified_names = f.read().splitlines()
        
        # Rename the files based on the modified filenames
        for old_name, new_name in zip(file_list, modified_names):
            if old_name != new_name:
                os.rename(os.path.join(directory, old_name), os.path.join(directory, new_name))
        
        print("Files renamed successfully.")
        
    finally:
        # Clean up the temporary file
        os.remove(temp_file.name)

# Usage: python batchrename.py <directory> [<text_editor>]
if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python batchrename.py <directory> [<text_editor>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    text_editor = sys.argv[2] if len(sys.argv) == 3 else None
    
    if text_editor is None:
        available_editors = get_available_text_editors()
        
        print("Available text editors:")
        for i, editor in enumerate(available_editors, start=1):
            print(f"{i}. {editor}")
        
        selection = input("Select the text editor by entering its number: ")
        
        try:
            selection_index = int(selection) - 1
            if 0 <= selection_index < len(available_editors):
                text_editor = available_editors[selection_index]
            else:
                raise ValueError()
        except ValueError:
            print("Invalid selection.")
            sys.exit(1)
    
    batch_rename(directory, text_editor)

