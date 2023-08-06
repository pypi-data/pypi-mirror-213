copy TableC.dll %1%

copy GasPropertyC.dll %1%

copy FrameworkC.dll %1%

copy sqlite3.dll %1%

copy Components.dll %1%

copy Tools.dll %1%

@REM copy CoolPropFluids.csv %1%

copy CoolProp.dll %1%

copy EnginePerformC.dll %1%

copy engineCUDA.dll %1%

Xcopy /S /Y /F /H /v /e include %1%\include\

@REM copy *.pyi %1%