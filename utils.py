# forensic_tool_web/utils.py

import os
import datetime

def get_file_metadata(file_path):
    """Gathers metadata for a given file."""
    try:
        file_stat = os.stat(file_path)
        return {
            "File Name": os.path.basename(file_path),
            "File Size": file_stat.st_size,
            "File Path": os.path.abspath(file_path),
            "Last Modified Time": datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "File Type/Extension": os.path.splitext(file_path)[1]
        }
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error getting metadata for {file_path}: {e}")
        return None

def format_size(size_bytes):
    """Formats file size into a human-readable format."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
