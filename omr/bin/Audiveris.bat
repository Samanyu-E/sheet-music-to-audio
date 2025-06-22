@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      https://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%"=="" @echo off
@rem ##########################################################################
@rem
@rem  Audiveris startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%"=="" set DIRNAME=.
@rem This is normally unused
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Resolve any "." and ".." in APP_HOME to make it shorter.
for %%i in ("%APP_HOME%") do set APP_HOME=%%~fi

@rem Add default JVM options here. You can also use JAVA_OPTS and AUDIVERIS_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS="--add-exports=java.desktop/sun.awt.image=ALL-UNNAMED"

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if %ERRORLEVEL% equ 0 goto execute

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto execute

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:execute

@rem Start script customization ---

@rem Actual value for min_java_version is to be provided by script post-processing
set /a min_java_version=21

for /f tokens^=2-5^ delims^=.-_^" %%j in ('"%JAVA_EXE%" -fullversion 2^>^&1') do (
    set "full_version=%%j.%%k.%%l-%%m"
    set "version=%%j"
)

if %version% LSS %min_java_version% (
    echo WARNING:
    echo WARNING: Current Java version %version% is lower than required %min_java_version%
    echo WARNING: Please install Java version %min_java_version% or higher
    echo WARNING:
@rem    start cmd /c "@echo off & mode con cols=50 lines=10 & echo // & echo // Audiveris WARNING: & echo // & echo // Your Java version is %version% (%full_version%) & echo // Please, install Java %min_java_version% or above. & echo // & pause"
    pause
    goto fail
)

@rem Stop script customization ---

@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\audiveris.jar;%APP_HOME%\lib\args4j-2.33.jar;%APP_HOME%\lib\logback-classic-1.4.14.jar;%APP_HOME%\lib\jai-imageio-jpeg2000-1.4.0.jar;%APP_HOME%\lib\jai-imageio-core-1.4.0.jar;%APP_HOME%\lib\itextpdf-5.5.13.2.jar;%APP_HOME%\lib\jgoodies-forms-1.9.0.jar;%APP_HOME%\lib\jgoodies-looks-2.7.0.jar;%APP_HOME%\lib\jaxb-core-2.3.0.1.jar;%APP_HOME%\lib\jaxb-impl-2.3.1.jar;%APP_HOME%\lib\jama-1.0.3.jar;%APP_HOME%\lib\jai-core-1.1.3.jar;%APP_HOME%\lib\jaxb-api-2.3.1.jar;%APP_HOME%\lib\ij-1.53j.jar;%APP_HOME%\lib\jcip-annotations-1.0.jar;%APP_HOME%\lib\org.apache.commons.io-2.4.jar;%APP_HOME%\lib\jbig2-imageio-3.0.4.jar;%APP_HOME%\lib\pdfbox-3.0.4.jar;%APP_HOME%\lib\fontbox-3.0.4.jar;%APP_HOME%\lib\pdfbox-io-3.0.4.jar;%APP_HOME%\lib\proxymusic-4.0.3.jar;%APP_HOME%\lib\eventbus-1.4.jar;%APP_HOME%\lib\tesseract-5.3.1-1.5.9.jar;%APP_HOME%\lib\tesseract-5.3.1-1.5.9-windows-x86_64.jar;%APP_HOME%\lib\leptonica-1.83.0-1.5.9.jar;%APP_HOME%\lib\leptonica-1.83.0-1.5.9-windows-x86_64.jar;%APP_HOME%\lib\javacpp-1.5.9.jar;%APP_HOME%\lib\bsaf-1.9.2.jar;%APP_HOME%\lib\jfreechart-1.5.3.jar;%APP_HOME%\lib\jgrapht-core-1.5.1.jar;%APP_HOME%\lib\github-api-1.301.jar;%APP_HOME%\lib\reflections-0.10.2.jar;%APP_HOME%\lib\slf4j-api-2.0.16.jar;%APP_HOME%\lib\logback-core-1.4.14.jar;%APP_HOME%\lib\jgoodies-common-1.8.1.jar;%APP_HOME%\lib\javax.activation-api-1.2.0.jar;%APP_HOME%\lib\commons-io-2.8.0.jar;%APP_HOME%\lib\commons-logging-1.3.4.jar;%APP_HOME%\lib\jaxb-runtime-4.0.5.jar;%APP_HOME%\lib\jaxb-core-4.0.5.jar;%APP_HOME%\lib\jakarta.xml.bind-api-4.0.2.jar;%APP_HOME%\lib\jheaps-0.13.jar;%APP_HOME%\lib\commons-lang3-3.9.jar;%APP_HOME%\lib\jackson-annotations-2.13.0.jar;%APP_HOME%\lib\jackson-core-2.13.0.jar;%APP_HOME%\lib\jackson-databind-2.13.0.jar;%APP_HOME%\lib\javassist-3.28.0-GA.jar;%APP_HOME%\lib\jsr305-3.0.2.jar;%APP_HOME%\lib\angus-activation-2.0.2.jar;%APP_HOME%\lib\jakarta.activation-api-2.1.3.jar;%APP_HOME%\lib\txw2-4.0.5.jar;%APP_HOME%\lib\istack-commons-runtime-4.1.2.jar


@rem Execute Audiveris
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %AUDIVERIS_OPTS%  -classpath "%CLASSPATH%" Audiveris %*

:end
@rem End local scope for the variables with windows NT shell
if %ERRORLEVEL% equ 0 goto mainEnd

:fail
rem Set variable AUDIVERIS_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% equ 0 set EXIT_CODE=1
if not ""=="%AUDIVERIS_EXIT_CONSOLE%" exit %EXIT_CODE%
exit /b %EXIT_CODE%

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
