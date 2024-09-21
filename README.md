# Control de Micrófono para Windows

Control de Micrófono es una aplicación de escritorio desarrollada en Python que permite a los usuarios controlar fácilmente el volumen y el estado de silencio de sus micrófonos en Windows. La aplicación utiliza una arquitectura hexagonal y ofrece una interfaz gráfica intuitiva.

## Características

- Control de volumen del micrófono con atajos de teclado personalizables
- Silenciar/Activar el micrófono con un atajo de teclado
- Interfaz gráfica de usuario intuitiva
- Tooltips con iconos del sistema para mostrar el estado del micrófono
- Alertas visuales integradas en la interfaz
- Funciona en la bandeja del sistema para un acceso rápido
- Soporte para múltiples dispositivos de entrada de audio

## Requisitos previos

- Python 3.7+
- Windows 10 o superior

## Instalación

1. Clona este repositorio o descarga el código fuente.
2. Navega hasta el directorio del proyecto.
3. Instala las dependencias necesarias:

```
pip install -r requirements.txt
```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando en el directorio raíz del proyecto:

```
python main.py
```

Una vez iniciada, la aplicación aparecerá en la bandeja del sistema. Puedes acceder a la ventana principal haciendo clic en el icono de la bandeja.

### Configuración

1. Selecciona el micrófono que deseas controlar en el menú desplegable.
2. Ajusta el paso de volumen según tus preferencias.
3. Configura los atajos de teclado para subir/bajar volumen y silenciar/activar el micrófono.
4. Haz clic en "Guardar configuración" para aplicar los cambios.

### Atajos de teclado

Los atajos de teclado predeterminados son:

- Subir volumen: (personalizable)
- Bajar volumen: (personalizable)
- Silenciar/Activar: (personalizable)

Puedes cambiar estos atajos en la ventana principal de la aplicación.

## Estructura del proyecto

El proyecto sigue una arquitectura hexagonal (puertos y adaptadores):

- `src/`
  - `domain/`: Entidades y puertos del dominio
  - `application/`: Servicios de aplicación
  - `infrastructure/`: Adaptadores para interactuar con el sistema
  - `interfaces/`: Interfaz gráfica de usuario
- `main.py`: Punto de entrada de la aplicación

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de enviar un pull request.

## Licencia

[MIT License](LICENSE)

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue en este repositorio.
