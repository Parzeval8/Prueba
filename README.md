# Task manager

Aplicativo web, que permite el registro, inicio de sesión y cierre de sesión de usuarios, así como la creación, visualización, actualización y el borrado de tareas.

## Instalación

1. Clona este repositorio: `git clone https://github.com/Parzeval8/Prueba.git`
2. Ve al directorio raiz del proyecto
3. Crea un entorno virtual (opcional pero recomendado): `python -m venv venv`
4. Activa el entorno virtual:
   - En Windows: `venv\Scripts\activate`
5. Instala los requisitos del proyecto: `pip install -r requirements.txt`

## Ejecución

1. Ejecuta las migraciones de la base de datos: `python manage.py migrate`
2. Inicia el servidor de desarrollo: `python manage.py runserver`

El proyecto estará disponible en `http://localhost:8000/`.

## Uso

- Accede a la aplicación en tu navegador web visitando `http://localhost:8000/`.