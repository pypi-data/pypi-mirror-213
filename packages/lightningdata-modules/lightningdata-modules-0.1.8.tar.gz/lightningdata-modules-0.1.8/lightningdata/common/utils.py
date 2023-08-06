import urllib.request
from getfilelistpy import getfilelist
from os import path, makedirs


def gdrive_download_domain_dataset(remote_folder: str,
                                   local_dir: str,
                                   domain: str,
                                   gdrive_api_key: str = None,
                                   debug_en: bool = False):
    success = True
    if debug_en:
        print('[DEBUG] Downloading: %s --> %s' % (remote_folder, local_dir))
    else:
        try:
            resource = {
                "api_key": gdrive_api_key,
                "id": remote_folder.split('/')[-1].split('?')[0],
                "fields": "files(name,id)",
            }
            res = getfilelist.GetFileList(resource)
            destination = local_dir
            if not path.exists(destination):
                makedirs(destination)
            domain_idx = 0
            available_domains = ""
            for index, name in enumerate(res['folderTree']['names']):
                if index != 0:
                    available_domains += name + " "
                if name == domain:
                    domain_idx = index
            if domain_idx == 0:
                print("Could not resolve domain name. Available domains are: " + available_domains)
                return False

            for file_dict in res['fileList'][domain_idx]['files']:
                print('Downloading %s' % file_dict['name'])
                if gdrive_api_key:
                    source = "https://www.googleapis.com/drive/v3/files/%s?alt=media&key=%s" % (file_dict['id'], gdrive_api_key)
                else:
                    source = "https://drive.google.com/uc?id=%s&export=download" % file_dict['id']  # only works for small files (<100MB)

            destination_folder = path.join(destination, domain)
            if not path.exists(destination_folder):
                makedirs(destination_folder)

            destination_file = path.join(destination_folder, file_dict['name'])
            if not path.isfile(destination_file):
                urllib.request.urlretrieve(source, destination_file)
            else:
                print("Dataset already downloaded")
                return True

        except Exception as err:
            print(err)
            success = False

    return success

