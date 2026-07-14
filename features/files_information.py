from pathlib import Path


HOME_DIR = Path.home()

def filepath_validation(path):
    clean_filepath = Path(path).resolve()
    result = {"valid_boundary": None,
              "message": "",
              "file_exists": None,
              "resolved_filepath": clean_filepath}

    if clean_filepath.is_relative_to(HOME_DIR):
        result["valid_boundary"] = True
        result["message"] = f'"{clean_filepath}" is within the home directory and is a "safe" filepath'
        if clean_filepath.exists():
            result["file_exists"] = True
            result["message"] = f'"{clean_filepath}" is safe, valid, and a workable filepath.'
        else:
            result["file_exists"] = False
            result["message"] = f'"{clean_filepath}" is an invalid filepath.'
    else:
        result["valid_boundary"] = False
        result["message"] = f'The filepath "{clean_filepath}" is outside the safe domain and is deemed a "dangerous" filepath.'

    return result
    
def list_directory(path):
    result = {"status": None,
              "message": "",
              "contents": []
    }
    verify_filepath = filepath_validation(path)
    if verify_filepath["valid_boundary"] and verify_filepath["file_exists"]:
        if verify_filepath["resolved_filepath"].is_dir():
            result["status"] = True 
            result["message"] = "The filepath is a valid directory"
            result["contents"] = list(verify_filepath["resolved_filepath"].iterdir())
        else:
            result["status"] = False
            result["message"] = "The filepath is not a valid directory"
    else:
        result["status"] = False
        result["message"] = verify_filepath["message"]
        
    return result

def search_content(name):
    content = f"*{name}*"
    all_contents = HOME_DIR.rglob(content)
    results = {"found": None,
               "status": "",
               "matches": []}

    results["matches"] = list(all_contents)
    
    if len(results["matches"]) == 0:
        results["found"] = False
        results["status"] = f'No matches were found with the content name "{name}".'
    else:
        results["found"] = True
        results["status"] = f'There are a total number of {len(results["matches"])} content(s) found with the content name "{name}".'
    
    return results