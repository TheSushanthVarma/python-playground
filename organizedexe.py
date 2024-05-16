import os

# get all extensions from a folder
def GetAllExtensions(dir,expect):
    import re
    FileList = []
    Extlist = []
    for fname in os.listdir(dir):
        FileList.append(fname)
        match = re.search(r'\.(.+)$',fname)       
        if match:
            if match.group(1) != expect:
                Extlist.append(match.group(1))
            elif None == expect:
                Extlist.append(match.group(1))
            else:
                pass
    return Extlist

LocationToBeOrganised = '.'
FileExtensions = GetAllExtensions("./",'py') #None
# FileExtensions is not Empty do this, if Empty 
if FileExtensions != []:
    try:
        for extension in FileExtensions: # ext have to be the folder name "ext's"
            ExtensionFileName = f"{extension}'s"
            for fname in os.listdir('.'):
                if fname.endswith(f'.{extension}'):
                    path = os.path.join(LocationToBeOrganised,ExtensionFileName) ; print(f'Found - {fname}')
                    if os.path.exists(path) != True:
                        os.mkdir(path) ; print(f'Folder Created  For {extension}')
                        os.replace(f"{LocationToBeOrganised}/{fname}",f"{ExtensionFileName}/{fname}")
                    else:
                        os.replace(f"{LocationToBeOrganised}/{fname}",f"{ExtensionFileName}/{fname}")
                else: 
                    pass
    except Exception as e:
        print(e)
else:
    print('No new files found!')
