import os
import platform
import shutil
import zipfile

from glob import glob

pyver = platform.python_version_tuple()[0] + platform.python_version_tuple()[1]

# clean Python library zip archive

PATH = 'dist/Syncplay.app/Contents/Resources/lib'

zin = zipfile.ZipFile(f'{PATH}/python{pyver}.zip', 'r')
tbd = [path for path in zin.namelist() if 'PySide2/Qt/' in path]

zout = zipfile.ZipFile(f'{PATH}/python{pyver}_new.zip', 'w', zipfile.ZIP_DEFLATED)

for item in zin.namelist():
    buffer = zin.read(item)
    if item not in tbd:
        zout.writestr(item, buffer)

zout.close()
zin.close()

os.remove(f'{PATH}/python{pyver}.zip')
os.rename(f'{PATH}/python{pyver}_new.zip', f'{PATH}/python{pyver}.zip')

# clean Frameworks folder

PATH = 'dist/Syncplay.app/Contents/Frameworks'

to_be_kept = ['QtCore', 'QtDBus', 'QtGui', 'QtNetwork', 'QtPrintSupport', 'QtQml', 'QtWidgets']
to_be_deleted = []

for f in glob(f'{PATH}/Qt*'):
    if not any({k in f for k in to_be_kept}):
        to_be_deleted.append(f)

for p in to_be_deleted:
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)
    else:
        os.remove(p)

# Clean PySide2 folder

PATH = 'dist/Syncplay.app/Contents/Resources/lib/python3.9/PySide2'

shutil.rmtree(f'{PATH}/examples', ignore_errors=True)

to_be_kept = ['QtCore', 'QtDBus', 'QtGui', 'QtNetwork', 'QtPrintSupport', 'QtQml', 'QtWidgets']
to_be_deleted = []

for f in glob(f'{PATH}/Qt*'):
    if not any({k in f for k in to_be_kept}):
        to_be_deleted.append(f)

for p in to_be_deleted:
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)
    else:
        os.remove(p)

# move .so from Framework to PySide2 folder

FROM = 'dist/Syncplay.app/Contents/Frameworks'
TO = 'dist/Syncplay.app/Contents/Resources/lib/python3.9/PySide2'

for f in glob(f'{FROM}/Qt*.so'):
    fn = os.path.basename(f)
    shutil.move(f, f'{TO}/{fn}')
