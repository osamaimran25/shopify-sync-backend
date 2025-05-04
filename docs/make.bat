@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation


if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build -c .
)
set SOURCEDIR=_source
set BUILDDIR=_build
<<<<<<< HEAD
set APP=..\shopify_sync_backend
=======
set APP=..\synch_backend
>>>>>>> df22a06b37407ac0c1e9773f7ff916f345cfe58f

if "%1" == "" goto html

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.Install sphinx-autobuild for live serving.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -b %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:livehtml
sphinx-autobuild -b html --open-browser -p 9000 --watch %APP% -c . %SOURCEDIR% %BUILDDIR%/html
GOTO :EOF

:apidocs
sphinx-apidoc -o %SOURCEDIR%/api %APP%
GOTO :EOF

:html
%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
