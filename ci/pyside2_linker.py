import os
from PySide2.QtCore import QLibraryInfo

def make_symlink(source, target):
    if os.path.islink(target):
        os.unlink(target)

    os.symlink(source, target)

QT_LIB_PATH = QLibraryInfo.location(QLibraryInfo.LibrariesPath)

frameworks = [elem for elem in os.listdir(QT_LIB_PATH) if '.framework' in elem]

os.chdir(QT_LIB_PATH)

for fr in frameworks:
    fr_path = os.path.join(QT_LIB_PATH, fr)
    fr_name = fr.split('.framework')[0]
    os.chdir(fr_path)
    if 'Versions'  in os.listdir('.'):
        make_symlink(f'Versions/Current/{fr_name}', fr_name)
        os.chdir(os.path.join(fr_path, 'Versions'))
        make_symlink('5', 'Current')
    os.chdir(QT_LIB_PATH)
