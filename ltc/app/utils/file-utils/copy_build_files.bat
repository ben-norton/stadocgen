@echo off

set SOURCE=G:\repos\tdwg\stadocgen\ltc\app\build
set TARGET=G:\repos\tdwg\ltc\docs
set LOGFILE=copy-log.log

ROBOCOPY %SOURCE% %TARGET% /COPY:DT /E /log:%LOGFILE%
