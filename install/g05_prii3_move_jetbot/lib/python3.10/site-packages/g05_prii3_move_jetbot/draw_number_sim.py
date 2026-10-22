import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class DrawNumberJetbotSim(Node):
    def __init__(self):
        super().__init__('draw_number_jetbot_sim')
        # Publicador de velocidades para el simulador del Jetbot
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Nodo de simulación 'draw_number' para el Jetbot iniciado.")
        
        # Temporizador para iniciar la secuencia de dibujo
        self.timer = self.create_timer(1.0, self.execute_drawing_sequence)
        self.sequence_executed = False

    def send_velocity(self, linear, angular, duration):
        """Envía comandos de velocidad durante un tiempo determinado."""
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)
        
        start_time = time.time()
        # Bucle de publicación constante durante el tiempo estimado
        while time.time() - start_time < duration:
            self.publisher_.publish(msg)
            time.sleep(0.05)
            
        # Detener motores al terminar el tramo
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        time.sleep(0.2)  # Pequeña pausa de estabilidad entre tramos

    def execute_drawing_sequence(self):
        if self.sequence_executed:
            return
        
        self.sequence_executed = True
        self.get_logger().info("Iniciando la trayectoria del número 5 en el Jetbot...")

        # --- Secuencia aproximada para dibujar el número 5 ---
        # 1. Avanzar recto (trazo superior horizontal)
        self.send_velocity(linear=0.2, angular=0.0, duration=1.5)
        
        # 2. Girar hacia abajo
        self.send_velocity(linear=0.0, angular=-1.57, duration=1.0)
        
        # 3. Avanzar (palo vertical superior corto)
        self.send_velocity(linear=0.2, angular=0.0, duration=1.0)
        
        # 4. Girar para hacer la curva de la tripa del 5
        self.send_velocity(linear=0.0, angular=-1.57, duration=1.0)
        
        # 5. Avanzar la base del bucle
        self.send_velocity(linear=0.2, angular=0.0, duration=1.5)
        
        # 6. Cerrar el bucle girando
        self.send_velocity(linear=0.0, angular=-3.14, duration=1.0)

        self.get_logger().info("¡Trayectoria del número 5 completada con éxito!")
        # Cancelar el temporizador para que no se repita
        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = DrawNumberJetbotSim()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()