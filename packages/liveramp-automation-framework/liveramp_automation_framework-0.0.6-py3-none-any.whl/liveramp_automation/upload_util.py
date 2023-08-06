import glob
import os
from datetime import datetime
from google.cloud import storage
from liveramp_automation.time_util import MACROS


def upload_to_bucket(src_path, dest_bucket_name, dest_path):
    bucket = storage.Client().bucket(dest_bucket_name)
    if os.path.isfile(src_path):
        blob = bucket.blob(os.path.join(dest_path, os.path.basename(src_path)))
        blob.upload_from_filename(src_path)
        return
    for item in glob.glob(src_path + '/*'):
        if os.path.isfile(item):
            if item == ".keep":
                continue
            blob = bucket.blob(os.path.join(dest_path, os.path.basename(item)))
            blob.upload_from_filename(item)
        else:
            upload_to_bucket(item, dest_bucket_name, os.path.join(dest_path, os.path.basename(item)))


def upload_files(dest_bucket_name):
    bucket = storage.Client().bucket(dest_bucket_name)
    prefix = (f"quality/")
    for filename in os.listdir('reports'):
        bucket.blob(f"{prefix}{filename}").upload_from_filename(f"./reports/{filename}")
