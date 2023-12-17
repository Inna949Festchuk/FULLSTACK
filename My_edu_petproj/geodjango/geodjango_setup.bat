set OSGEO4W_ROOT=C:\Program Files\QGIS 3.12
set PYTHON_ROOT=C:\Users\prepodavatel\AppData\Local\Programs\Python\Python38
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
set PATH=%PATH%;%PYTHON_ROOT%;%OSGEO4W_ROOT%\bin
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /f /d "%PATH%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v GDAL_DATA /t REG_EXPAND_SZ /f /d "%GDAL_DATA%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROJ_LIB /t REG_EXPAND_SZ /f /d "%PROJ_LIB%"

@REM set OSGEO4W_ROOT=/Applications/QGIS.app/Contents
@REM set PYTHON_ROOT=C:\Users\prepodavatel\AppData\Local\Programs\Python\Python38
@REM set GDAL_DATA=%OSGEO4W_ROOT%/Resources/gdal
@REM set PROJ_LIB=%OSGEO4W_ROOT%/Resources/proj
@REM set PATH=%PATH%;%PYTHON_ROOT%;%OSGEO4W_ROOT%/bin