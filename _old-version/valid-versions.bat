@echo off
echo Starting Versions Validation...

echo Checking package locked dependencies...
call npm run package:check
if errorlevel 1 (
    echo package lock check failed!
    exit /b 1
)
if errorlevel 1 (
    exit /b 1
)

exit /b 0