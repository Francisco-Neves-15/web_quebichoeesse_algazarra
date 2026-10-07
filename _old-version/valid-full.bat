@echo off

echo Running build check (validates CSS, PostCSS, and Next.js config)...
call npm run build:check
if errorlevel 1 (
    echo Build check failed! This may indicate CSS import errors, PostCSS issues, or other runtime errors.
    exit /b 1
)

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