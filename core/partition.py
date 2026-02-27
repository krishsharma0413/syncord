from core.discord_handler import upload_files, bulk_download_files
from core.encrypter import encrypted_data, decrypted_data
from core.db_manager import SQliteDB
from core.setup import BASE_DIR
from uuid import uuid4
from math import ceil
import os

PER_PARTITION_SIZE = int(5 * 1024 * 1024)  # 5 MB

def download_file_by_path(file_path: str, path_to_download:str="."):
    # future proofing code
    folder = "default"
    print(file_path)
    if "/" in file_path:
        folder = "/".join(file_path.split("/")[:-1])
        file_path = file_path.split("/")[-1]
    database = SQliteDB()
    f = False
    for x in database.get_file_by_file_path(folder, file_path):
        assemble_partition(x[1], path_to_download=path_to_download)
        f = True
        break
    if not f:
        print("File not found in database.")

def download_folder_by_path(folder: str, files_by_folder: dict=None):
    if files_by_folder is None:
        database = SQliteDB()
        files = database.get_all_folder_files(folder)
        files_by_folder = {folder: files}
        
        print(files_by_folder)
    print(files_by_folder)
    
    for file in files_by_folder.get(folder, []):
        print(f"Downloading file: {file[4]}/{file[3]}")
        download_file_by_path(file[1], path_to_download="./"+folder)
    
def assemble_partition(partition_uuid, path_to_download:str="."):
    """
    assemble the file back with the help of parition uuid.
    - read partition_uuid from DB first
    - retrieves the data from discord and save it into /files folder
    - sends the list of newly generated files to assemble_files()
    end goal: Saves the file to the current path itself.
    """
    database = SQliteDB()
    records = database.get_file_by_parition_id(partition_uuid)

    message_ids = []
    for record in records:
        message_ids.append(record[2])

    file_name = record[3]
    os.makedirs(BASE_DIR / "files" / partition_uuid, exist_ok=True)
    files = bulk_download_files(message_ids, partition_uuid)

    return assemble_files(files, file_name, path_to_download)


def assemble_files(files: list[str], filename: str, path_to_download:str="."):
    """
    - gets the files path IN ORDER from assemble_parition()
    - save the files to the current path and delete the /files partitioned files
    """
    with open(f"{path_to_download}/{filename}", "wb") as final_file:
        for x in files:
            with open(x, "rb") as bin_file:
                encypt = bin_file.read()
                decrypt = decrypted_data(encypt)
                final_file.write(decrypt)

    # delete partitioned files
    partition_dir = os.path.dirname(files[0])
    for x in files:
        os.remove(x)

    os.rmdir(partition_dir)
    return True

def partition_file(file_path, folder_name="default"):
    """
    parition the files into chunks if required and sends this to upload_partitions()
    """
    partition_uuid = str(uuid4())
    number_of_partitions = ceil((os.stat(file_path).st_size / (1024 * 1024)) / 5)

    output_dir = BASE_DIR / "files" / partition_uuid
    os.makedirs(output_dir, exist_ok=True)

    files = []

    try:
        with open(file_path, "rb") as bin_file:

            for x in range(number_of_partitions):
            
                with open(BASE_DIR / "files" / partition_uuid / f"{x}.bin", "wb") as temp_bin:
                    # ensures that anyone cannot just download your data
                    # from discord and compile themselves
                    non_ecrypt = bin_file.read(PER_PARTITION_SIZE)
                    encrypt = encrypted_data(non_ecrypt)
                    temp_bin.write(encrypt)
                    files.append(BASE_DIR / "files" / partition_uuid / f"{x}.bin")
                    print(f"Created partition number {x}: {BASE_DIR / 'files' / partition_uuid / f'{x}.bin'}")

        return upload_partitions(files, partition_uuid, file_path, folder_name)
    
    except PermissionError as e:
        print(e)


def upload_partitions(files: list[str], partition_uuid: str, file_path: str, folder_name: str):
    """
    - upload to discord + save to DB
    """
    print("Uploading partitions to Discord...")
    message_ids = upload_files(files)
    database = SQliteDB()
    i = 0
    for file, msg_id in zip(files, message_ids):
        database.add_file(
            partition_number = i,
            partition_uuid = partition_uuid,
            message_id = msg_id,
            file_name = file_path.split("/")[-1].split("\\")[-1],
            folder_name = folder_name,
            file_size_bytes = os.stat(file).st_size
        )
        print(f"Saved partition {i} info to database.")
        i += 1

    partition_dir = os.path.dirname(files[0])
    for x in files:
        os.remove(x)

    os.rmdir(partition_dir)

    return message_ids


if __name__ == "__main__":
    # test partition_file()
    files = partition_file("testing.mp4")
    print(files)
    # assemble_files(files, "end_result_testing.mp4")
