from .files_information import filepath_validation

AVAILABLE_FILETYPES = [".py", ".txt", ".pdf", ".md", ".c", ".sh", ".go"]

def read_files(file, num_lines=None):
    results = {
        "verification_status": None,
        "valid_filetype": None,
        "message": "",
        "content": None
               }
    verification = filepath_validation(file)
    lines = []
    if verification["valid_boundary"] and verification["filepath_exists"]: 
        if verification["resolved_filepath"].is_file():
            results["verification_status"] = True
            results["message"] = f'The filepath "{verification["resolved_filepath"]}" is a file.'
            get_fileextension = verification["resolved_filepath"].suffix

            if get_fileextension in AVAILABLE_FILETYPES:
                results["valid_filetype"] = True
                results["message"] = f'The filetype "{get_fileextension}" is a valid filetype.'
                with open (verification["resolved_filepath"], "r") as f:
                    if num_lines != None:
                        for line in f:
                            lines.append(line)
                            if len(lines) == num_lines:
                                break
                        content = "".join(lines)
                    else:
                        content = f.read()
                    results["content"] = content
            else:
                results["valid_filetype"] = False
                results["message"] = f'The filetype "{get_fileextension}" is an invalid filetype.'
        else:
            results["verification_status"] = False
            results["message"] = f'The filepath "{verification["resolved_filepath"]}" is not a file.'
    else:
        results["verification_status"] = False
        results["message"] = verification["message"]
    
    return results


def write_and_edit_files(file, mode=None):
    results = {
        "verification_status": None,
        "message": "",
        "mode": "",
        "updated_content": None
    }

    verification = filepath_validation(file)
    if verification["valid_boundary"] and verification["file_exists"]:
        if verification["resolved_filepath"].is_file():
            verification["verifcation_status"] = True
    else:
        results["verification_status"] = False
        results["message"] = verification["message"]