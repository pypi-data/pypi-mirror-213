from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
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
    Executable('sound_source_id\\__main__.py',
               base=base,
               target_name = 'sound_source_id',
               icon='icons/point-right.ico')
]

setup(name='sound_source_id',
    version="0.0.13",
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
