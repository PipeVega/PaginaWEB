rmdir /s /q .venv
call python -m pip install --upgrade pip
call pip install --upgrade virtualenv
call python -m venv .venv
call .venv\Scripts\activate.bat
call python -m pip install --upgrade pip
call pip install django
call pip install pillow
call pip install djangorestframework
call pip install transbank-sdk
call pip install django-extensions