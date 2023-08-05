import os
import hashlib

from django.conf import settings
from .settings_models import TREE_DRIECTORY_TABLE, DIRECTORY_TREE_MODEL_USE

def find_url_in_database(attachmet_path):
    for key, value in TREE_DRIECTORY_TABLE.items():
        for field in value['fields']:
            kwargs = {
                '{}'.format(field): attachmet_path,
            }
            result = value['model'].objects.filter(**kwargs).first()
            if result:
                return "{} ({} {})".format(value['model'].__name__, field, result.pk)
    return None
class GetListInFolder():
    
    def __init__(self, path_in):
        self.path = os.path.join(settings.MEDIA_ROOT, path_in)
        self.list = self.list_dir(self.path)

    def join_path(self, base, folder):
        return os.path.join(base, folder)

    def get_file_size(self, path):
        '''
            1KB = 1024 Byte
            1MB = 1024 KB ( 1024 Byte * 1024 Byte ) = 1,048,576 Byte
            1GB = 1024 MB ( 1024 Byte * 1024 Byte * 1024 Byte ) = 1,073,741,824 Byte
        '''
        file_size = os.path.getsize(path)
        unit_power = ["Byte", "KB", "MB", "GB"]
        for power in range(len(unit_power)-1, 0, -1): # GB -> KB
            result = file_size / 1024**power
            if int(result) >= 1:
                return "{} {}".format(float("{:.2f}".format(result)), unit_power[power])

        return "{} {}".format(file_size, unit_power[0])
        
    def contain_detail(self, item, path, type="folder"):
        url = settings.MEDIA_URL + path.replace(settings.MEDIA_ROOT, "").replace("\\", "/")[1:]
        temp = {
            "key_id": hashlib.md5("{} {}".format(type, url).encode('utf-8')).hexdigest(),
            "type": type,
            "name": item,
            "url": url,
        }
        if type == "file":
            temp["size"] = self.get_file_size(path)
        if type == "folder":
            temp["url"] = path.replace(settings.MEDIA_ROOT, "").replace("\\", "/")[1:]

        return temp

    def list_dir(self, path):
        list_dir = os.listdir( path )
        folders = []
        files = []
        for item in list_dir:
            attachmet_path = self.join_path(path, item)
            if os.path.isdir(attachmet_path):
                folders.append(self.contain_detail(item, attachmet_path, "folder"))
            else:
                result_dict = self.contain_detail(item, attachmet_path, "file")
                if DIRECTORY_TREE_MODEL_USE:
                    result = find_url_in_database(attachmet_path.replace(settings.MEDIA_ROOT, "").replace("\\", "/")[1:])
                    if result:
                        result_dict['from'] = result

                files.append(result_dict)
        
        return folders + files

    def get(self):
        return self.list