from pathlib import Path
from pypdf import PdfReader 
from constants import HOME_DIR, EXCLUDED1, EXCLUDED2


def filepath_validation(path):
    clear_filepath = (HOME_DIR / path).resolve()

    if path == "." or path == "~":
        clear_filepath = HOME_DIR.resolve()
    

    result = {"valid_boundary": None,
              "message": "",
              "filepath_exists": None,
              "resolved_filepath": clear_filepath}

    if clear_filepath.is_relative_to(HOME_DIR):
        result["valid_boundary"] = True
        result["message"] = f'"{clear_filepath}" is within the home directory and is a "safe" filepath'
        if clear_filepath.exists():
            result["filepath_exists"] = True
            result["message"] = f'"{clear_filepath}" is safe, valid, and a workable filepath.'
        else:
            result["filepath_exists"] = False
            result["message"] = f'"{clear_filepath}" is an invalid filepath.'
    else:
        result["valid_boundary"] = False
        result["message"] = f'The filepath "{clear_filepath}" is outside the safe domain and is deemed a "dangerous" filepath.'

    return result
    
def list_directory(path):
    result = {"status": None,
              "message": "",
              "contents": []
    }
    verify_filepath = filepath_validation(path)
    if verify_filepath["valid_boundary"] and verify_filepath["filepath_exists"]:
        if verify_filepath["resolved_filepath"].is_dir():
            result["status"] = True 
            result["message"] = f'The filepath "{verify_filepath["resolved_filepath"]}" is a valid directory.'
            contents = verify_filepath["resolved_filepath"].iterdir()
            for c in contents:
                if not any(part in EXCLUDED1 for part in c.parts) and not any(part in EXCLUDED2 for part in c.parts):
                    result["contents"].append(c)
        else:
            result["status"] = False
            result["message"] = "The filepath is not a valid directory."
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
    
    for c in all_contents:
        if not any(part in EXCLUDED1 for part in c.parts) and not any(part in EXCLUDED2 for part in c.parts):
            results["matches"].append(c)

    
    if len(results["matches"]) == 0:
        results["found"] = False
        results["status"] = f'No matches were found with the content name "{name}".'
    else:
        results["found"] = True
        results["status"] = f'There are a total number of {len(results["matches"])} content(s) found with the content name "{name}".'
    
    return results