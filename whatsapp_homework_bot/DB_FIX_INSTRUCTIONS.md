# Solución para el Error de Base de Datos ("no such table")

El error `OperationalError: no such table: user` significa que la base de datos está vacía y no tiene las tablas (`user`, `grade`, etc.). El log que me enviaste del `flask db upgrade` se ve incompleto, lo que sugiere que no se ejecutó correctamente la primera vez.

**Vamos a solucionarlo de forma definitiva.** Por favor, sigue estos pasos en orden exacto para recrear la base de datos desde cero.

---

### **Pasos para Reparar la Base de Datos**

1.  **Detén el servidor** si está corriendo (presionando `Ctrl+C` en la terminal).

2.  **Elimina la base de datos y las migraciones anteriores.** Esto nos dará un inicio completamente limpio. Ejecuta estos comandos en tu terminal (asegúrate de estar en la carpeta raíz del proyecto, la que contiene el `.git`):

    *   **En Windows:**
        ```bash
        del whatsapp_homework_bot\app.db
        rd /s /q migrations
        ```

    *   *(Si alguno de los comandos da un error de "no encontrado", no te preocupes y simplemente continúa con el siguiente paso)*.

3.  **Establece la variable de entorno de Flask (muy importante):**
    ```bash
    set FLASK_APP=whatsapp_homework_bot/run.py
    ```

4.  **Inicializa el entorno de migración desde cero:**
    ```bash
    flask db init
    ```

5.  **Crea el primer archivo de migración:**
    ```bash
    flask db migrate -m "Initial migration"
    ```

6.  **Aplica la migración para crear las tablas:** **Este es el paso más importante.**
    ```bash
    flask db upgrade
    ```
    Ahora deberías ver un output más largo, indicando que se están aplicando los cambios al crear las tablas.

7.  **Crea el usuario administrador:**
    ```bash
    flask create-admin admin adminpass
    ```

8.  **Carga los grados:**
    ```bash
    flask seed-grades
    ```

9.  **Inicia la aplicación:**
    ```bash
    python whatsapp_homework_bot/run.py
    ```

Después de este proceso completo, la base de datos se habrá recreado desde cero y de forma correcta. El inicio de sesión debería funcionar sin problemas.
