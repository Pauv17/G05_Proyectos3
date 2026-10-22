import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class CollisionAvoidanceJetbotSim(Node):
    def __init__(self):
        super().__init__('collision_avoidance_jetbot_sim')
        
        # Publicador para enviar velocidades al simulador del Jetbot
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Suscriptor al tópico del LiDAR (/scan)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Distancia de seguridad en metros (si hay un obstáculo a menos de 0.3m, frena)
        self.safe_distance = 0.3
        self.obstacle_detected = False
        
        # Temporizador para evaluar el movimiento constantemente (cada 0.1 segundos)
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Nodo de evitación de obstáculos (simulación Jetbot) iniciado.")

    def scan_callback(self, msg: LaserScan):
        try:
            # Seleccionamos el rango frontal del LiDAR (delante del robot)
            # Dependiendo de cómo simule el LiDAR el Jetbot, el frente suele estar al inicio o al final del array
            front_ranges = msg.ranges[0:15] + msg.ranges[-15:]
            
            # Filtramos valores no válidos (inf o nan) dentro del rango del sensor
            valid_ranges = [r for r in front_ranges if r > msg.range_min and r < msg.range_max]
            
            if valid_ranges:
                min_distance = min(valid_ranges)
                # Comprobamos si el obstáculo está demasiado cerca
                if min_distance < self.safe_distance:
                    self.obstacle_detected = True
                else:
                    self.obstacle_detected = False
            else:
                self.obstacle_detected = False
                
        except Exception as e:
            self.obstacle_detected = False

    def control_loop(self):
        msg = Twist()
        
        if self.obstacle_detected:
            # Si hay obstáculo: detener completamente el robot
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().warn("¡Obstáculo detectado en simulación! Frenando...", throttle_duration_sec=1.0)
        else:
            # Si el camino está libre: avanzar de forma autónoma
            msg.linear.x = 0.15
            msg.angular.z = 0.0
            
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceJetbotSim()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()