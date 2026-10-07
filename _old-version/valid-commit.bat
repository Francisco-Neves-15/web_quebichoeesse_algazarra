@echo off

call valid-common.bat
if errorlevel 1 (
    exit /b 1
)

echo Formatting code...
call npm run format:fix
if errorlevel 1 (
    echo Format failed!
    exit /b 1
)

echo All validations passed!
exit /b 0