@echo off
rem ===================================================================
rem  Local preview - double-click to build and view the docs site.
rem  (Chinese instructions: see the "how to view the docs" page on the site)
rem
rem  Why not just double-click site\index.html?
rem  MkDocs writes links in "directory" form (animation/level-sequence/),
rem  but the real file on disk is animation/level-sequence/index.html.
rem  Only an HTTP server performs that mapping; the file:// protocol just
rem  shows a folder listing. So we start a tiny local server instead.
rem
rem  Uses only Python's standard library - nothing to install.
rem
rem  NOTE: keep this file ASCII-only. The console codepage on this machine
rem  is 936 (GBK), and mixing encodings here makes cmd.exe mis-parse lines.
rem ===================================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/2] Building site  ^(mkdocs build --clean^)
echo.
call mkdocs build --clean
if errorlevel 1 (
  echo.
  echo   BUILD FAILED - fix the errors above, then run this file again.
  echo.
  pause
  exit /b 1
)

echo.
echo [2/2] Starting local preview ...
echo.
echo     URL    http://127.0.0.1:8000/
echo     STOP   close this window  ^(or press Ctrl+C^)
echo.
echo   Port already in use? An older preview window is probably still open.
echo.

start "" http://127.0.0.1:8000/
python -m http.server 8000 --directory site

echo.
echo Preview stopped.
pause
