install with

```curl -LJ https://github.com/vakkD/chat/blob/main/scriptname.exe?raw=true -o chat.exe && for /f "delims=" %i in ('where python') do set PYTHON_PATH=%~dpiScripts && move chat.exe "%PYTHON_PATH%"```
