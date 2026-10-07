@echo off
echo Starting validation...

call valid-common.bat
if errorlevel 1 (
    echo "--> error: If there are errors in validator.ts, run `npm run build:check` to rebuild..."
    exit /b 1
)

echo All validations passed!
exit /b 0