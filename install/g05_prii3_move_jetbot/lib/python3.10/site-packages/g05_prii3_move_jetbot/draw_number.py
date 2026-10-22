import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class DrawNumberJetbot(Node):
    def __init__(self):
        super().__init__('draw_number_node')
        # Publicador de velocidades para el Jetbot (/cmd_vel)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info("Nodo draw_number (Jetbot) iniciado.")
        
        self.timer = self.create_timer(1.0, self.execute_sequence)
        self.executed = False

    def send_velocity(self, linear, angular, duration):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher_.publish(msg)
            time.sleep(0.05)
            
        # Detener motores al terminar el tramo
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        time.sleep(0.2)

    def execute_sequence(self):
        if self.executed:
            return
        self.executed = True
        
        self.get_logger().info("Ejecutando trayectoria del número en el Jetbot...")
        
        # Secuencia de movimientos para dibujar el número
        self.send_velocity(linear=0.15, angular=0.0, duration=1.5)
        self.send_velocity(linear=0.0, angular=-1.57, duration=1.0)
        self.send_velocity(linear=0.15, angular=0.0, duration=1.0)
        self.send_velocity(linear=0.0, angular=-1.57, duration=1.0)
        self.send_velocity(linear=0.15, angular=0.0, duration=1.5)
        
        self.get_logger().info("¡Trayectoria finalizada!")
        self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = DrawNumberJetbot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()