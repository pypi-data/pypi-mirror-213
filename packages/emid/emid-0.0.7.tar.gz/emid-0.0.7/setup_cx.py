from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['emid',
                              'soundfile'],
                 'excludes': ['tkinter',
                              'PyQt5.QtQml',
                              'PyQt5.QtBluetooth',
                              'PyQt5.QtQuickWidgets',
                              'PyQt5.QtSensors',
                              'PyQt5.QtSerialPort',
                              'PyQt5.QtSql'
                              ]}


import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('emid\\__main__.py',
               base=base,
               target_name = 'emid',
               icon='icons/oem-face-neutral.ico')
]

setup(name='emid',
    version="0.0.7",
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
