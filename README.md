# Proyecto RII 3: Robots Inteligentes - Sprint 1

**Grupo 05**

Este repositorio contiene el paquete de ROS2 (`g05_prii3_turtlesim`) desarrollado para el Sprint 1. El objetivo es controlar de forma autónoma el simulador `turtlesim` para dibujar un trayecto predefinido mediante un nodo implementado en Python.

## Requisitos del Sistema
* **Sistema Operativo:** Ubuntu 22.04
* **Framework:** ROS2 Humble

## Instrucciones de Instalación y Compilación

1. Crear el espacio de trabajo (workspace) y acceder a la carpeta de código fuente:
   mkdir -p ~/g05_prii3_ws/src
   cd ~/g05_prii3_ws/src

2. Clonar este repositorio dentro del directorio `src`:
   git clone [https://github.com/Pauv17/G05_Proyectos3.git](https://github.com/Pauv17/G05_Proyectos3.git)
   

3. Volver a la raíz del espacio de trabajo y compilar el paquete:
   
   cd ~/g05_prii3_ws
   colcon build
  

4. Cargar las variables de entorno del espacio de trabajo recién compilado:
   bash
   source install/setup.bash
   

## Ejecución del Proyecto

El sistema está configurado para ejecutarse mediante un único archivo launch, el cual inicializa el simulador y el nodo de control de forma simultánea.

Para arrancar el proyecto, ejecuta el siguiente comando en la terminal (asegurándote de haber realizado el paso 4 previamente):

bash
ros2 launch g05_prii3_turtlesim dibujo.launch.py


## Control de la Trayectoria (Servicios)

El nodo expone servicios ROS que permiten interactuar con el dibujo en tiempo real. Para utilizarlos, abre una nueva terminal, carga las variables de entorno (`source ~/g05_prii3_ws/install/setup.bash`) y ejecuta los siguientes comandos según la acción deseada:

* **Pausar el movimiento de la tortuga:**
  bash
  ros2 service call /pausar_dibujo std_srvs/srv/SetBool "{data: true}"
  

* **Reanudar el movimiento:**
  bash
  ros2 service call /pausar_dibujo std_srvs/srv/SetBool "{data: false}"
  

* **Reiniciar el dibujo desde el inicio:**
  bash
  ros2 service call /reiniciar_dibujo std_srvs/srv/Trigger
  
