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


def create_and_edit_files(file, content=None, mode=None):
    results = {
        "verification_status": None,
        "message": "",
        "valid_filetype": None,
        "mode": mode,
        "updated_content": None
    }

    verification = filepath_validation(file)

    if verification["valid_boundary"]:
        if mode == "create":
            if verification["filepath_exists"]:
                results["verification_status"] = False
                results["message"] = "Error. Can't create an already existing file."
            else:
               results["verification_status"] = True
               verification["resolved_filepath"].touch()
               get_parentdirectory = verification["resolved_filepath"].parent
               results["message"] = f'A new file called "{verification["resolved_filepath"].name}" has been created in the directory "{get_parentdirectory}".'
               results["updated_content"] = None    

        elif mode == "edit":
            if verification["filepath_exists"]:
                if verification["resolved_filepath"].is_file():
                    results["verification_status"] = True
                    results["message"] = "The filepath is an existing file that can be safely edited."
                    get_fileextension = verification["resolved_filepath"].suffix
                    if get_fileextension in AVAILABLE_FILETYPES:
                        results["valid_filetype"] = True
                        results["message"] = f'The filetype "{get_fileextension}" is a valid filetype.'
                        with open (verification["resolved_filepath"], "a") as f:
                            if content is not None:
                                results["updated_content"]  = f.write(content)
                    else:
                        results["valid_filetype"] = False
                        results["message"] = f'The filetype "{get_fileextension}" is an invalid filetype.'
                else:
                    results["verification_status"] = False
                    results["message"] = f'The filepath "{verification["resolved_filepath"]}" is not a file.'  
            else:
                results["verification_status"] = False
                results["message"] = f'The filepath "{verification["resolved_filepath"]}" does not exist.'

        elif mode == None:
            results["message"] = "No mode provided."

        else:
            results["message"] = "Invalid mode."

    else:
        results["verification_status"] = False
        results["message"] = verification["message"]
    
    return results

def bookbot(file):
    results = {
        "verification_status": None,
        "message": "",
        "characters_count": {},
        "words_count": {}
    }
    verification = filepath_validation(file)
    if verification["valid_boundary"] and verification["filepath_exists"]:
        if verification["resolved_filepath"].is_file():
            results["verification_status"] = True
            get_fileextension = verification["resolved_filepath"].suffix
            if get_fileextension == ".txt" or get_fileextension == ".pdf" or get_fileextension == ".md":
                read_filecontent = read_files(verification["resolved_filepath"])
                sentences = read_filecontent["content"].split("\n")
                for sentence in sentences:
                    for word in sentence:
                        if word in results["words_count"]:
                            results["words_count"][word] += 1
                        else:
                             results["words_count"][word] = 1
                        for char in word:
                            if char in results["characters_count"]:
                                results["characters_count"][char] += 1
                            else:
                                results["characters_count"][char] = 1
            else:
                results["message"] = f'The filetype "{get_fileextension} is not a readable paragraph filetype.'
        else:
            results["verification_status"] = False
            results["message"] = f'The filepath "{verification["resolved_filepath"]}" is not a file.'
    else:
        results["verification_status"] = False
        results["message"] = verification["message"]
    
    return results