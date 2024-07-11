@echo off
call cls
echo.
echo Por medio de este archivo graph.bat podras generar una imagen .png del diagrama de clases de tus modelos Django.
echo.
echo Si quieres leer el articulo original que explica como hacerlo, puedes revisar en la carpeta graph el documento:
echo.
echo "Generar diagramas de clase UML a partir de modelos Django.docx"
echo.
echo Para que todo funcione bien, primero debes realizar los siguientes pasos:
echo.
echo 1. Instalar en tu computador Graphviz 32-bits
echo    Lo puedes descargar desde https://graphviz.org/download/
echo    Tambien te deje una copia del instalador en la carpeta graph, que se llama:
echo    "windows_10_cmake_Release_graphviz-install-8.0.5-win32.exe"
echo.
echo 2. Si quieres puedes instalar los fonts Roboto para que no aparezcan warnings al generar la imagen
echo    Para instalar los fonts Roboto, tienes que descomprimir roboto.zip que esta en la carpeta graph 
echo    y hacer CLIC DERECHO + INSTALAR sobre cada archivo .ttf
echo.
echo 3. Este proyecto Django ya tiene instalada la biblioteca "pydotplus" necesaria para generar la imagen
echo.
echo 4. Este archivo .bat ejecutara el siguiente comando que creara el archivo "tienda_diagrama_clases.png"
echo.
echo    "python manage.py graph_models -a -o tienda_diagrama_clases.png"
echo.
echo Presiona [ENTER] para crear y abrir el archivo "tienda_diagrama_clases.png"
echo.
pause
call C:\ProyectosDjango\tienda\.venv\Scripts\activate.bat
call python manage.py graph_models -a -o tienda_diagrama_clases.png
call tienda_models.png