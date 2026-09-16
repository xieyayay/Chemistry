@echo off
rem ===================================================================
rem  Build the offline demo copy of the docs site.
rem
rem  Why a second build?
rem  The normal site uses directory-style links (systems/task-system/).
rem  Only a web server maps those to index.html -- double-clicking them
rem  just shows a folder listing. This build switches to .html links so
rem  the whole folder works without any server, which is what you want
rem  for demoing, or for sending the site to someone to look at.
rem
rem  Output: site-offline\        <- for showing people
rem          site\                <- for the server (built by the preview script)
rem  Do NOT deploy site-offline\ -- it is the demo copy.
rem
rem  Keep this file ASCII-only and CRLF. The console codepage here is
rem  936 (GBK) and mixing encodings makes cmd.exe mis-parse lines.
rem ===================================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/2] Building the offline demo copy ...
echo.
call mkdocs build -f mkdocs.offline.yml --clean
if errorlevel 1 (
  echo.
  echo   BUILD FAILED - fix the errors above, then run this file again.
  echo.
  pause
  exit /b 1
)

echo.
echo [2/2] Done.
echo.
echo   Folder      site-offline\
echo   Open it by double-clicking   site-offline\index.html
echo   You can zip the whole site-offline folder and send it to anyone.
echo.
echo   NOTE: this copy is for demoing only. The version to deploy to a
echo         server is the  site\  folder.
echo.

start "" "site-offline"
echo Press any key to close this window.
pause >nul
