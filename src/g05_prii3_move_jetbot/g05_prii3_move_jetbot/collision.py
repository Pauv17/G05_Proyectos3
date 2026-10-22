import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class CollisionAvoidanceJetbot(Node):
    def __init__(self):
        super().__init__('collision_avoidance_node')
        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        self.safe_distance = 0.3  # Distancia de seguridad en metros
        self.obstacle_detected = False
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Nodo de evitación de colisiones (collision.py) iniciado.")

    def scan_callback(self, msg: LaserScan):
        try:
            # Evaluar el rango frontal del LiDAR
            front_ranges = msg.ranges[0:15] + msg.ranges[-15:]
            valid_ranges = [r for r in front_ranges if r > msg.range_min and r < msg.range_max]
            
            if valid_ranges and min(valid_ranges) < self.safe_distance:
                self.obstacle_detected = True
            else:
                self.obstacle_detected = False
        except Exception:
            self.obstacle_detected = False

    def control_loop(self):
        msg = Twist()
        if self.obstacle_detected:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().warn("¡Obstáculo enfrente! Frenando...", throttle_duration_sec=1.0)
        else:
            msg.linear.x = 0.12
            msg.angular.z = 0.0
            
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceJetbot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()