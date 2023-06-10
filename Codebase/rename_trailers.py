import os

def rename_trailer_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            original_name, extension = os.path.splitext(file)
            if '- trailer' in original_name:
                new_name = original_name.replace('- trailer', '-trailer')
                new_file = new_name + extension
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_file)
                os.rename(old_path, new_path)
                print(f"Renamed file: {old_path} -> {new_path}")

# Example usage
folder_path = "/Volumes/Backup Plus/Movies"
rename_trailer_files(folder_path)