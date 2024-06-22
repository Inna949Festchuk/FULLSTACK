python manage.py import_json -c@REM set OSGEO4W_ROOT=C:\Program Files\QGIS 3.12
@REM set PYTHON_ROOT=C:\Users\prepodavatel\AppData\Local\Programs\Python\Python38
@REM set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
@REM set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
@REM set PATH=%PATH%;%PYTHON_ROOT%;%OSGEO4W_ROOT%\bin
@REM reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /f /d "%PATH%"
@REM reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v GDAL_DATA /t REG_EXPAND_SZ /f /d "%GDAL_DATA%"
@REM reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROJ_LIB /t REG_EXPAND_SZ /f /d "%PROJ_LIB%"
set OSGEO4W_ROOT=C:\Program Files\PostgreSQL\10
set PYTHON_ROOT=C:\Users\prepodavatel\AppData\Local\Programs\Python\Python38
set GDAL_DATA=%OSGEO4W_ROOT%\gdal-data
set PROJ_LIB=%OSGEO4W_ROOT%\share\contrib\postgis-3.2\proj
set PATH=%PATH%;%PYTHON_ROOT%;%OSGEO4W_ROOT%\bin;
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /f /d "%PATH%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v GDAL_DATA /t REG_EXPAND_SZ /f /d "%GDAL_DATA%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROJ_LIB /t REG_EXPAND_SZ /f /d "%PROJ_LIB%"