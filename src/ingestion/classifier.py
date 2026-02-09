import magic
import os
import logging


def handle_dropped_paths(path_list, progress_callback=None): # thinking this will be a list when GUI is in place
    
    if isinstance(path_list, str):
        path_list = [path_list]

    if not isinstance(path_list, list):
        return "Error: path_list must be a list"

    results = []
    total_files = len(path_list)

    for index, path in enumerate(path_list):
        status = {
            "path": os.path.basename(path),
            "full_path": path,
            "type": None,
            "status": "success",
            "error": None
        }


        if not os.path.exists(path):
            status["status"] = "error"
            status["error"] = "File not found"
        else:
            try:
                status["type"] = identify_mime_type(path)
            except Exception as e:
                status["status"] = "error"
                status["error"] = str(e)

        results.append(status)

        if progress_callback:
            progress_callback(index + 1, total_files, status["path"])

    return results


def identify_mime_type(path):

    ALLOWED_TYPES = {
        'application/pdf': 'PDF',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
        'text/csv': 'CSV',
        'text/plain': 'CSV'
            }

    mime = magic.Magic(mime=True)

    try:
        file_type = mime.from_file(path)

        return ALLOWED_TYPES.get(file_type)

    except Exception as e:
        return f"Error: {str(e)}"


