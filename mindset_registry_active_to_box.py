#!/usr/bin/env python3

# ummap_mri_scan_report_to_box.py


# Import modules

from boxsdk.exception import BoxAPIException

import box_config


# Box Client

# Get authenticated client
client = box_config.get_authenticated_client(box_config.pathToConfigJson)

# Define local file to upload
local_file_dir = "/home/airflow/scripts/MiNDSet_Registry_Active"
local_file_path = local_file_dir + "/MiNDSet_Registry_Active.csv"

# Define Box folder ID and file ID
folder_id = '107501141140'
file_id = '637162037867'

# Upload UMMAP_MRIScanReport.csv to Box
try:
    new_file = client.file(file_id).update_contents(local_file_path)
except BoxAPIException as e:
    print(e.context_info)
    print(f"File {local_file_path} doesn't exist on Box. Uploading new file.")
    new_file = client.folder(folder_id).upload(local_file_path)

print(f"File {new_file.name} uploaded to Box with file ID {new_file.id}.")