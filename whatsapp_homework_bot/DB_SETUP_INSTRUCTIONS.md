# Pasos para Crear la Base de Datos e Insertar Registros

¡Excelente! Con las librerías instaladas, estos son los siguientes pasos. Es muy importante que los ejecutes en **orden** y desde la **carpeta raíz de tu proyecto** (la que contiene el `.git`).

---

### **Paso 1: Establecer la Variable de Entorno**

Este comando le dice a Flask dónde encontrar tu aplicación. Debes ejecutarlo cada vez que abras una nueva terminal.

*   En la terminal de Windows (CMD):
    ```bash
    set FLASK_APP=whatsapp_homework_bot/run.py
    ```

### **Paso 2: Crear la Estructura de la Base de Datos**

Estos comandos crean las tablas vacías.

1.  **Inicializar el directorio de migraciones:**
    ```bash
    flask db init
    ```
    *(Nota: Si ya existe la carpeta `migrations`, este comando dará un error. No te preocupes y puedes continuar si es el caso)*.

2.  **Crear el archivo de migración:**
    ```bash
    flask db migrate -m "Initial database setup"
    ```

3.  **Aplicar la migración para crear las tablas:**
    ```bash
    flask db upgrade
    ```

### **Paso 3: Insertar los Registros Iniciales**

Estos comandos añaden los datos necesarios para empezar.

1.  **Crear el usuario administrador:**
    ```bash
    flask create-admin admin adminpass
    ```

2.  **Cargar los grados escolares:**
    ```bash
    flask seed-grades
    ```

---

### **Paso 4: ¡Ejecutar!**

Una vez completados todos los pasos anteriores, tu base de datos estará lista. Ahora puedes iniciar la aplicación:

```bash
python whatsapp_homework_bot/run.py
```

Y luego podrás entrar en `http://localhost:5000` con el usuario `admin` y la contraseña `adminpass`.
