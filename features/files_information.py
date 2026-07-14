from pathlib import Path


HOME_DIR = Path.home()

def filepath_validation(path):
    clean_filepath = Path(path).resolve()
    boundary_check = [None, ""]
    fileexistence_check = [None, ""]


    if clean_filepath.is_relative_to(HOME_DIR):
        boundary_check[0] = True
        boundary_check[1] = f'"{clean_filepath}" is within the home directory and is a "safe" filepath'
        if clean_filepath.exists():
            fileexistence_check[0] = True
            fileexistence_check[1] = f'"{clean_filepath}" is a valid and workable filepath.'
        else:
            fileexistence_check[0] = False
            fileexistence_check[1] = f'"{clean_filepath}" is an invalid filepath.'
        return fileexistence_check[0], fileexistence_check[1]
    else:
        boundary_check[0] = False
        boundary_check[1] = f'The filepath "{clean_filepath}" is outside the safe domain and is deemed a "dangerous" filepath.'
    return boundary_check[0], boundary_check[1], clean_filepath
    
def list_directory(path):
    valid_state, feedback, resolved_path = filepath_validation(path)
    if valid_state:
        if resolved_path.is_dir():
            contents = list(resolved_path.iterdir())
            return contents
        else:
            raise Exception("The filepath is not a valid directory")
    raise Exception(feedback)

def search_content(content):
    pass
    