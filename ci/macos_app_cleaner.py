import os
import platform
import shutil

from glob import glob

pyver = platform.python_version_tuple()[0] + '.' +  platform.python_version_tuple()[1]

# Clean resources

PATH = 'dist/Syncplay.app/Contents/Resources/'

to_be_kept = []
to_be_deleted = []

for f in glob(f'{PATH}/qt*'):
    if not any({k in f for k in to_be_kept}):
        to_be_deleted.append(f)

for p in to_be_deleted:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            os.remove(p)

# Clean PySide6 folder

PATH = f'dist/Syncplay.app/Contents/Resources/lib/python{pyver}/PySide6'

shutil.rmtree(f'{PATH}/examples', ignore_errors=True)
shutil.rmtree(f'{PATH}/include', ignore_errors=True)

to_be_kept = ['QtCore', 'QtGui', 'QtWidgets']
to_be_deleted = []

for f in glob(f'{PATH}/Qt*'):
    if not any({k in f for k in to_be_kept}):
        to_be_deleted.append(f)

for a in glob(f'{PATH}/*.app'):
    to_be_deleted.append(a)

to_be_deleted.remove(f'{PATH}/Qt')
to_be_deleted.extend([f'{PATH}/lupdate', f'{PATH}/qmllint', f'{PATH}/lrelease'])

for p in to_be_deleted:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            os.remove(p)

# Clean PySide6/Qt folder

PATH = f'dist/Syncplay.app/Contents/Resources/lib/python{pyver}/PySide6/Qt'

to_be_deleted.extend([f'{PATH}/qml', f'{PATH}/translations'])

for p in to_be_deleted:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            os.remove(p)

# Clean PySide6/Qt/lib folder

PATH = f'dist/Syncplay.app/Contents/Resources/lib/python{pyver}/PySide6/Qt/lib'

to_be_kept = ['QtCore', 'QtDBus', 'QtGui', 'QtWidgets']
to_be_deleted = [f'{PATH}/metatypes']

for f in glob(f'{PATH}/Qt*'):
    if not any({k in f for k in to_be_kept}):
        to_be_deleted.append(f)

for p in to_be_deleted:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            os.remove(p)

# Clean PySide6/Qt/plugins folder

PATH = f'dist/Syncplay.app/Contents/Resources/lib/python{pyver}/PySide6/Qt/plugins'

to_be_kept = ['platforms', 'styles']
to_be_deleted = []

for f in glob(f'{PATH}/*'):
    if not any({k in f for k in to_be_kept}):
        to_be_deleted.append(f)

for p in to_be_deleted:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
        else:
            os.remove(p)

# symlink .so from shiboken6 to PySide6 folder

cwd = os.getcwd()

FROM = f'dist/Syncplay.app/Contents/Resources/lib/python{pyver}/shiboken6'
TO = f'dist/Syncplay.app/Contents/Resources/lib/python{pyver}/PySide6'

fn = os.path.basename(glob(f'{FROM}/libshiboken6*.dylib')[0])

os.chdir(TO)
os.symlink(f'../shiboken6/{fn}', f'./{fn}')
os.chdir(cwd)
