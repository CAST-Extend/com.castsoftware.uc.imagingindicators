@echo off
REM Provide the path of the python.exe which is installed under CAST folder, main.py file as per your system, Schema_prefix, host ,port,user, password
set python_abs_path="C:\work\servtool_179 Imaging Indicator Version 1.0.4 Changes\com.castsoftware.uc.imagingindicators\com.castsoftware.uc.imagingindicatorsbatchtool\Python310\python.exe"

set application_schema_prefix="webgoat_v8_2_2"
set local_DB_name="postgres"
set local_DB_host="localhost"
set local_DB_port=2284
set local_DB_user="operator"
set local_DB_password="CastAIP"
set console_url="http://localhost:8081"
set console_username="admin"
set console_password="admin"
set central_DB_name="postgres"
set central_DB_host="tooling3" 
set central_DB_port=2284 
set central_DB_user="operator" 
set central_DB_password="CastAIP"

%python_abs_path% "C:\work\servtool_179 Imaging Indicator Version 1.0.4 Changes\com.castsoftware.uc.imagingindicators\com.castsoftware.uc.imagingindicatorsbatchtool\main.py" %application_schema_prefix% %local_DB_name% %local_DB_host% %local_DB_port% %local_DB_user% %local_DB_password% %console_url% %console_username% %console_password% %central_DB_name% %central_DB_host% %central_DB_port% %central_DB_user% %central_DB_password%

pause