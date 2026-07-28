from .files_information import filepath_validation
from constants import AVAILABLE_FILETYPES, AVAILABLE_IMAGETYPES, AVAILABLE_CODINGFILETYPES, UNACCEPTABLE_PATTERNS, CONVERSION_REFUSED
from pypdf import PdfReader
from pathlib import Path
import base64  

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
                if get_fileextension == ".pdf":
                    read_pdf = PdfReader(verification["resolved_filepath"])
                    text = []
                    for page in read_pdf.pages:
                        text.append(page.extract_text())
                    pdf_content = "\n".join(text)
                    results["content"] = pdf_content
                else:
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
                    words = sentence.split() 
                    for word in words:
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
                results["verification_status"] = False
                results["message"] = f'The filetype "{get_fileextension} is not a readable paragraph filetype.'
        else:
            results["verification_status"] = False
            results["message"] = f'The filepath "{verification["resolved_filepath"]}" is not a file.'
    else:
        results["verification_status"] = False
        results["message"] = verification["message"]
    
    return results


def read_images(image):
    
    results = {
        "verification_status": None,
        "message": "",
        "valid_imagetype": None,
        "encoded_data": "",
        "mime_type": None

    }
    verification = filepath_validation(image)
    if verification["valid_boundary"] and verification["filepath_exists"]:
        if verification["resolved_filepath"].is_file():
            get_fileextension = verification["resolved_filepath"].suffix
            if get_fileextension in AVAILABLE_IMAGETYPES:
                results["verification_status"] = True
                results["valid_imagetype"] = True
                results["message"] = f'The filepath "{verification["resolved_filepath"]}" is a valid image file.'
                if get_fileextension == ".jpg":
                    results["mime_type"] = "image/jpeg"
                else:
                    results["mime_type"] = f"image/{get_fileextension[1:]}"
                with open (verification["resolved_filepath"], "rb") as f:
                    read_binarydata = f.read()
                    encode_binarydata = base64.b64encode(read_binarydata)
                    decoded_datastring = encode_binarydata.decode("utf-8")
                    results["encoded_data"] = decoded_datastring
            else: 
                results["verification_status"] = False
                results["valid_imagetype"] = False
                results["message"] = f'The filepath "{verification["resolved_filepath"]}" is an invalid image file or is not a file.'
        else:
            results["verification_status"] = False
            results["valid_imagetype"] = False
            results["message"] = f'The filepath "{verification["resolved_filepath"]}" is not a valid filep or could be a directory.'
    else:
        results["verification_status"] = False
        results["message"] = verification["message"]
    
    return results

def convert_codingfile(filepath, target_language, client, model):
    results = {
        "valid_coding_language": None,
        "verification_status": None,
        "message": "",
        "content": "",
    }
    coding_languages = {
        ".py": "Python",
        ".c": "C",
        ".go": "GoLang",
        ".sh": "Shell Script"
    }
    language_to_extension = {
        "python": ".py",
        "go": ".go",
        "c": ".c",
        "shell": ".sh"
    }
    
    filepath = Path(filepath)
    get_fileextension = filepath.suffix
    if get_fileextension in AVAILABLE_CODINGFILETYPES:
        source_language = coding_languages[get_fileextension]
        results["valid_coding_language"] = True
        source_file = read_files(filepath)
        if source_file["verification_status"] and source_file["valid_filetype"]:
            results["verification_status"] = True
            results["message"] = f'The filepath "{filepath.resolve()}" is an existing valid filepath and is a supported coding language file.'
            source_code = source_file["content"]
            sentences = source_code.split("\n")
            unaccepted_pattern_found = False
            for sentence in sentences:
                for pattern in UNACCEPTABLE_PATTERNS:
                    if pattern in sentence:
                        unaccepted_pattern_found = True
                        break
                if unaccepted_pattern_found:
                    break
            if unaccepted_pattern_found:
                results["verification_status"] = False
                results["message"] = "This file contains patterns not supported for conversion (e.g. file I/O, OS access)."
            else:
                prompt = f"""You are converting a self-contained coding problem solution from {source_language} to {target_language}.

Only perform this conversion if the code represents a self-contained algorithmic solution, similar to a LeetCode or Codewars problem — no file I/O, external libraries, interactive input, or OS-level operations. If the code does not fit this pattern, respond with exactly: {CONVERSION_REFUSED}

Otherwise, respond with ONLY the converted {target_language} code. Do not include explanations, comments about the conversion process, or markdown code fences.

Here is the code to convert:

{source_code}
"""         
                response = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
                converted_code = response.choices[0].message.content
                target_extension = language_to_extension.get(target_language.lower().strip())
                if target_extension is None:
                    results["verification_status"] = False
                    results["message"] = "Unsupported coding file type."
                else:
                    new_filepath = filepath.with_suffix(target_extension)
    
                    if converted_code.strip() == CONVERSION_REFUSED:
                        results["verification_status"] = False
                        results["message"] = "The LLM determined this code is not a self-contained problem-solving solution and declined to convert it."
                    else:
                        create_newfile = create_and_edit_files(new_filepath, mode="create")
                        if create_newfile["verification_status"]:
                            edit_newfile = create_and_edit_files(new_filepath, content=converted_code, mode="edit")
                            if edit_newfile["verification_status"]:
                                results["verification_status"] = True
                                results["message"] = f'Successfully converted and saved to "{new_filepath}".'
                                results["content"] = converted_code
                            else:
                                results["verification_status"] = False
                                results["message"] = edit_newfile["message"]
                        else:
                            results["verification_status"] = False
                            results["message"] = create_newfile["message"]
        else:
            results["verification_status"] = False
            results["message"] = source_file["message"]
    else:
        results["valid_coding_language"] = False
        results["message"] = f'The filepath "{filepath}" is not a supported coding language file.'
    
    return results  