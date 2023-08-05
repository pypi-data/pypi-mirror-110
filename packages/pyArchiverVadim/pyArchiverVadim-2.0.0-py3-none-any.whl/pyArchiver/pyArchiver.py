import zipfile, os, pathlib


def to_zip(path_to_zip: str, objects: list):

    with zipfile.ZipFile(path_to_zip, 'w') as ZipArchive:
        for object in objects:
            if os.path.isdir(object):
                folder = os.path.abspath(object)
                for foldername, subfolders, filenames in os.walk(folder):

                    if foldername == folder:
                        archive_folder_name = ''
                    else:
                        archive_folder_name = os.path.relpath(foldername, folder)
                        ZipArchive.write(foldername, arcname=archive_folder_name)

                    for filename in filenames:
                        ZipArchive.write(os.path.join(foldername, filename), arcname=os.path.join(archive_folder_name, filename))
            elif os.path.isfile(object):
                ZipArchive.write(object, arcname=os.path.basename(object))
    

def unzipping(path_to_zip: str, where_to_extract: str = None):
    if where_to_extract == None:
        where_to_extract = path_to_zip
        output_name = os.path.splitext(os.path.basename(where_to_extract))[0]
        where_to_extract = pathlib.Path(path_to_zip).resolve().parent
        where_to_extract = os.path.join(where_to_extract, output_name)

    with zipfile.ZipFile(path_to_zip, 'r') as zipEx:
        zipEx.extractall(where_to_extract)

