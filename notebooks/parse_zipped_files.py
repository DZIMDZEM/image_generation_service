import os
import zipfile
import rarfile


def extract_obj_files(source_folder, target_folder):
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # List all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    for i, file in enumerate(files):
        # Construct full file path
        file_path = os.path.join(source_folder, file)

        try:
            # Check if the file is a ZIP file and process
            if file_path.lower().endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for zip_info in zip_ref.infolist():
                        if zip_info.filename.lower().endswith('.obj'):
                            # Strip path information
                            zip_info.filename = os.path.basename(zip_info.filename)
                            zip_ref.extract(zip_info, target_folder)

            # Check if the file is a RAR file and process
            elif file_path.lower().endswith('.rar'):
                with rarfile.RarFile(file_path, 'r') as rar_ref:
                    for rar_info in rar_ref.infolist():
                        if rar_info.filename.lower().endswith('.obj'):
                            # Strip path information
                            rar_info.filename = os.path.basename(rar_info.filename)
                            rar_ref.extract(rar_info, target_folder)

        except Exception as e:
            print(f"Failed to process {file_path}: {str(e)}")


# Usage
source_folder = r'C:\Users\dzmit\Downloads\3d-objects\processed_zip'
target_folder = r'C:\Users\dzmit\Downloads\3d-objects\parsed'

extract_obj_files(source_folder, target_folder)
