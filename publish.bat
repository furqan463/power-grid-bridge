@echo off
SETLOCAL EnableDelayedExpansion

echo ====================================================
echo  Power Grid Bridge - Automated Local PyPI Publisher
echo ====================================================

:: 1. Clean up old distribution builds to avoid uploading duplicates
if exist dist (
    echo [INFO] Cleaning up old distribution artifacts...
    rmdir /s /q dist
)
if exist build (
    rmdir /s /q build
)

:: 3. Build the source wheel and distribution
echo [INFO] Compiling build targets...
uv build
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build compilation failed. Aborting upload.
    pause
    exit /b %ERRORLEVEL%
)

:: 5. Validate the distribution metadata
echo [INFO] Verifying PyPI metadata consistency...
uv run py -m twine check dist/*
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Metadata check failed. Please review your pyproject.toml constraints.
    pause
    exit /b %ERRORLEVEL%
)

:: 6. Upload package to PyPI
echo.
echo ====================================================
echo  Ready for Upload!
echo  Reminder: Username is "__token__"
echo  Password is your pypi- API Token string.
echo ====================================================
echo.
uv run py -m twine upload dist/*

echo.
echo [SUCCESS] Distribution sequence complete.
pause