@echo off
set /p resposta=Você deseja limpar o arquivo JSON? (Y/N): 

if /i "%resposta%"=="Y" (
    echo {"last_folder": ""} > config.json
    echo Arquivo JSON limpo com sucesso.
) else (
    echo Operação cancelada. Nenhum arquivo foi alterado.
)

pause
