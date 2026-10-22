import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool, Trigger

class DrawNumber5(Node):
    def __init__(self):
        super().__init__('draw_number')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

        # Servicios para controlar el robot
        self.create_service(SetBool, 'pause_resume', self.pause_callback)
        self.create_service(Trigger, 'restart_draw', self.restart_callback)

       
        self.movimientos = [
            ("avanzar", 2.0),
            ("girar_izquierda", 3.1),
            ("avanzar", 2.0),
            ("girar_izquierda", 3.1),
            ("avanzar", 2.0),
            ("girar_derecha", 3.1),
            ("avanzar", 2.0),
            ("girar_derecha", 3.1),
            ("avanzar", 2.0)
        ]

        self.paso_actual = 0
        self.tiempo_transcurrido = 0.0
        self.is_paused = False

        self.dt = 0.1
        self.timer = self.create_timer(self.dt, self.timer_callback)
        
        self.get_logger().info('¡Nodo iniciado! Leyendo lista de movimientos...')

    def pause_callback(self, request, response):
        self.is_paused = request.data
        if self.is_paused:
            self.stop_robot()
            self.get_logger().info('PAUSADO. Se quedará donde está.')
        else:
            self.get_logger().info('REANUDADO. Continúa su camino.')
        response.success = True
        return response

    def restart_callback(self, request, response):
        self.paso_actual = 0
        self.tiempo_transcurrido = 0.0
        self.is_paused = False
        self.get_logger().info('REINICIADO. Empezando de nuevo desde el paso 0.')
        response.success = True
        return response

    def timer_callback(self):
        if self.is_paused:
            return 
        
        if self.paso_actual >= len(self.movimientos):
            self.stop_robot()
            return 

        accion, duracion = self.movimientos[self.paso_actual]
        

        msg = Twist()
        if accion == "avanzar":
            msg.linear.x = 0.2
            msg.angular.z = 0.0
        elif accion == "girar_izquierda":
            msg.linear.x = 0.0
            msg.angular.z = 0.5
        elif accion == "girar_derecha":
            msg.linear.x = 0.0
            msg.angular.z = -0.5
            
        self.publisher_.publish(msg)

        self.tiempo_transcurrido += self.dt

        if self.tiempo_transcurrido >= duracion:
            self.paso_actual += 1     
            self.tiempo_transcurrido = 0.0 
            self.stop_robot()            

    def stop_robot(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DrawNumber5()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
