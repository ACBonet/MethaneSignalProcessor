@echo off
echo Building Docker image...
docker build -t py2exe .

echo Running container to build .exe...
docker run --rm -v %cd%:/src py2exe

echo Executable generated: dist\main.exe
pause