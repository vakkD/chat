### command line chatgpt

install and update with

```curl -LJ https://github.com/vakkD/chat/blob/main/scriptname.exe?raw=true -o chat.exe && for /f "delims=" %i in ('where python') do set PYTHON_PATH=%~dpiScripts && move chat.exe "%PYTHON_PATH%"```

and run by calling 'chat' in terminal


pyinstaller:
C:\Users\dylan\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe" --onefile --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --hidden-import=termcolor --hidden-import=revchatgpt chat.py
