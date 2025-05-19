import os
import sys

# File extension categories
image_extensions = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.tiff', '.webp', '.heic', '.svg', '.ico',
    '.raw', '.psd', '.jfif'
]

document_extensions = [
    '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.ppt', '.pptx', '.odt', '.ods', '.rtf', '.csv',
    '.md', '.tex', '.epub'
]

video_extensions = [
    '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
    '.webm', '.3gp', '.mpeg', '.mpg', '.m4v', '.ts'
]

code_extensions = [
    '.py', '.js', '.ts', '.html', '.htm', '.css',
    '.c', '.cpp', '.h', '.hpp', '.cs', '.java',
    '.sh', '.bash', '.bat', '.cmd', '.php', '.rb',
    '.pl', '.json', '.xml', '.yml', '.yaml', '.swift',
    '.kt', '.kts', '.ini', '.env', '.toml', '.cfg',
    '.lua', '.md', '.rst', '.ipynb', '.vbs'
]

audio_extensions = [
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma',
    '.m4a', '.alac', '.aiff', '.opus', '.amr'
]

compressed_extensions = [
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
    '.xz', '.iso', '.lzma', '.cab', '.arj', '.tgz',
    '.tbz2'
]

executable_extensions = ['.exe', '.msi']

folder_map = {
    "Documents": document_extensions,
    "Audio": audio_extensions,
    "Code": code_extensions,
    "Vidéos": video_extensions,
    "Images": image_extensions,
    "Compressed": compressed_extensions,
    "Executable": executable_extensions,
    # No extensions listed for "Others" - it will catch everything else
}

def show_notification(title, message):
    """Show notification based on platform"""
    try:
        if sys.platform == 'win32':
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5)
        else:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                timeout=5
            )
    except ImportError:
        print(f"{title}: {message}")

def organize_files():
    """Organize files into categorized folders"""
    try:
        files = os.listdir(os.getcwd())
        moved_files = 0
        others_count = 0

        for filename in files:
            try:
                # Skip directories
                if os.path.isdir(filename):
                    continue
                    
                ext = os.path.splitext(filename)[1].lower()
                source = os.path.join(os.getcwd(), filename)
                
                if not os.path.exists(source):
                    print(f"File not found: {filename}")
                    continue
                
                # Skip the script itself
                if filename in ["main.py", "main.exe", os.path.basename(__file__)]:
                    continue
                
                file_moved = False
                for folder, extensions in folder_map.items():
                    if ext in extensions:
                        destination_folder = os.path.join(os.getcwd(), folder)
                        if not os.path.exists(destination_folder):
                            os.makedirs(destination_folder)
                        destination = os.path.join(destination_folder, filename)
                        os.replace(source, destination)
                        moved_files += 1
                        file_moved = True
                        break
                
                # If file didn't match any category, move to "Others"
                if not file_moved:
                    destination_folder = os.path.join(os.getcwd(), "Others")
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    destination = os.path.join(destination_folder, filename)
                    os.replace(source, destination)
                    moved_files += 1
                    others_count += 1
            
            except Exception as file_error:
                print(f"Error processing {filename}: {str(file_error)}")
                continue

        if moved_files > 0:
            message = f"Organized {moved_files} files successfully!"
            if others_count > 0:
                message += f" ({others_count} moved to Others)"
            show_notification("Success", message)
        else:
            show_notification("Info", "No files needed organizing.")

    except Exception as e:
        show_notification("Error", f"An error occurred: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    organize_files()