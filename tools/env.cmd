set PYROOT=D:\Python38
::set PYROOT=C:\Python27
::set PYROOT=C:\WinPython-64bit-2.7.13.1Zero\python-2.7.13.amd64
::set PYROOT=D:\WinPython-32bit-2.7.10.2\python-2.7.10set PYROOT=D:\WinPython-32bit-2.7.10.2\python-2.7.10
set PATH=%PYROOT%;%PYROOT%\Scripts;%PATH%;

set MYROOT=%~dp0..\
pushd %MYROOT%

::python.exe -m pip install --upgrade pip
::pip.exe install -U appdirs
::pip.exe install python-evtx
::pip.exe install tinydb
::pip.exe install requests
::pip.exe uninstall lxml
::pip.exe install lxml
::pip.exe install -U Cython
::pip.exe uninstall pyqt4
::pip.exe install C:\userdata\github\PyQt4-4.11.4-cp27-cp27m-win32.whl
::pip.exe uninstall pywin32
::pip.exe install pywin32
::pip.exe install -U PyInstaller
::pip.exe install -U -i https://pypi.tuna.tsinghua.edu.cn/simple setproctitle
::pip.exe install -U psutil
::pip.exe install -U fastapi

::pip.exe install -U ray[serve]
::pip.exe install -U joblib
::pip.exe install -U chardet
::pip.exe install -U pynsist
::pip.exe install pipdeptree
