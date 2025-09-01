# Instrucciones para Ejecutar y Probar la Aplicación

Aquí tienes los pasos detallados para poner en marcha y probar la aplicación.

---

### **Paso 1: Preparación del Entorno (Solo se hace la primera vez)**

Primero, necesitamos preparar todo. Abre una terminal y ejecuta los siguientes comandos uno por uno en el directorio raíz del proyecto:

1.  **Instalar las dependencias:**
    ```bash
    pip install -r whatsapp_homework_bot/requirements.txt
    ```

2.  **Configurar la variable de entorno de Flask:**
    *   En Linux o macOS:
        ```bash
        export FLASK_APP=whatsapp_homework_bot/run.py
        ```
    *   En Windows (Command Prompt):
        ```bash
        set FLASK_APP=whatsapp_homework_bot/run.py
        ```

3.  **Crear y actualizar la base de datos:** Este comando aplica todas las migraciones para crear las tablas.
    ```bash
    flask db upgrade
    ```

4.  **Crear tu usuario administrador:**
    ```bash
    flask create-admin admin adminpass
    ```
    *(Esto crea un usuario llamado `admin` con la contraseña `adminpass`. Puedes usar los que prefieras)*.

5.  **Cargar los grados escolares en la base de datos:**
    ```bash
    flask seed-grades
    ```

---

### **Paso 2: Ejecutar la Aplicación**

Una vez completada la preparación, ya puedes iniciar el servidor web y el programador de tareas con un solo comando:

```bash
python3 whatsapp_homework_bot/run.py
```

Verás mensajes en la consola indicando que el servidor está corriendo en `http://0.0.0.0:5000/` y que las tareas automáticas (envío de tareas y renovaciones) han sido programadas.

---

### **Paso 3: Probar la Funcionalidad en tu Navegador**

1.  Abre tu navegador web y ve a la dirección: **`http://localhost:5000`**
2.  Verás la página de **inicio de sesión**. Usa las credenciales que creaste:
    *   **Usuario:** `admin`
    *   **Contraseña:** `adminpass`
3.  Una vez dentro, estarás en el **Dashboard**. Haz clic en el botón azul **"+ Nueva Suscripción"**.
4.  Rellena el formulario con datos de prueba (un número de WhatsApp, un email y selecciona un grado) y haz clic en "Crear Suscripción".
5.  Serás redirigido de nuevo al dashboard. Verás tu nueva suscripción en la tabla con el estado **'pending'**.
6.  Haz clic en el botón **"Activar Manualmente"**. La página se recargará y verás que el estado de la suscripción ahora es **'active'**.

¡Felicidades! Con esto has probado el flujo principal de la aplicación.

---

### **Paso 4: Observar los Procesos Automáticos (Las Simulaciones)**

*   **Envío de Tareas:** La tarea de envío de tareas se ejecuta a las **2 PM** (14:00, hora de Colombia). Si dejas la aplicación corriendo, a esa hora verás en la **consola de la terminal** los mensajes de simulación, indicando que se han obtenido las tareas, se ha generado el audio y se ha "enviado" la notificación.
*   **Renovaciones:** La tarea de renovación se ejecuta a la **1 AM**. Si una suscripción está a punto de vencer, verás en la consola la simulación del intento de cobro.

Puedes detener la aplicación en cualquier momento presionando `Ctrl+C` en la terminal.
