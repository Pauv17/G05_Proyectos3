import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool, Trigger

class NodoG05(Node):
    def __init__(self):
        super().__init__('dibujante_g05')
        
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        self.srv_pausa = self.create_service(SetBool, 'pausar_dibujo', self.cb_pausar)
        self.srv_reinicio = self.create_service(Trigger, 'reiniciar_dibujo', self.cb_reiniciar)
        
        self.timer_period = 0.1
        self.timer = self.create_timer(self.timer_period, self.control_loop)
        
        self.en_pausa = False
        self.estado_actual = 0
        self.tiempo_en_estado = 0.0
        
        self.movimientos = [
            (0.0, 3.1416, 1.0),
            (2.0, 0.0, 1.0),
            (0.0, 1.5708, 1.0),
            (2.0, 0.0, 2.0),
            (0.0, 1.5708, 1.0),
            (2.0, 0.0, 1.0),
            (0.0, 1.5708, 1.0),
            (2.0, 0.0, 1.0),
            (0.0, 1.5708, 1.0),
            (2.0, 0.0, 0.5),
        ]

    def cb_pausar(self, request, response):
        self.en_pausa = request.data
        response.success = True
        response.message = "Dibujo pausado" if self.en_pausa else "Dibujo reanudado"
        self.get_logger().info(response.message)
        return response

    def cb_reiniciar(self, request, response):
        self.estado_actual = 0
        self.tiempo_en_estado = 0.0
        self.en_pausa = False
        response.success = True
        response.message = "Dibujo reiniciado desde el principio"
        self.get_logger().info(response.message)
        return response

    def control_loop(self):
        msg = Twist()
        
        if self.en_pausa:
            self.publisher_.publish(msg)
            return
            
        if self.estado_actual >= len(self.movimientos):
            self.publisher_.publish(msg)
            return
            
        v_lineal, v_angular, duracion = self.movimientos[self.estado_actual]
        
        msg.linear.x = v_lineal
        msg.angular.z = v_angular
        self.publisher_.publish(msg)
        
        self.tiempo_en_estado += self.timer_period
        
        if self.tiempo_en_estado >= duracion:
            self.estado_actual += 1
            self.tiempo_en_estado = 0.0

def main(args=None):
    rclpy.init(args=args)
    nodo = NodoG05()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
