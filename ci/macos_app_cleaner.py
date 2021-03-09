import os
import zipfile

PATH = 'dist/Syncplay.app/Contents/Resources/lib'

zin = zipfile.ZipFile(f'{PATH}/python37.zip', 'r')
tbd = [path for path in zin.namelist() if 'PySide2/Qt/' in path]

zout = zipfile.ZipFile(f'{PATH}/python37_new.zip', 'w', zipfile.ZIP_DEFLATED)

for item in zin.namelist():
    buffer = zin.read(item)
    if item not in tbd:
        zout.writestr(item, buffer)

zout.close()
zin.close()

os.remove(f'{PATH}/python37.zip')
os.rename(f'{PATH}/python37_new.zip', f'{PATH}/python37.zip')
