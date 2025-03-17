import rclpy
from rclpy.node import Node

import numpy as np # type: ignore

from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive


class SafetyNode(Node):
    """
    The class that handles emergency braking.
    """
    def __init__(self):
        super().__init__('safety_node')
        
        self.publisher_ = self.create_publisher(AckermannDriveStamped, 'drive',10)
#        self.speed = 0.

#        self.light_brake_used = False
#        self.emergency_brake_active = False 

        self.odom_subscription = self.create_subscription(Odometry, '/ego_racecar/odom', self.odom_callback, 10)
        self.scan_subscription = self.create_subscription(LaserScan, 'scan',self.scan_callback, 10)
        


    def odom_callback(self, msg):
        """
        Callback para lidar com os dados da odometria.
        """
        self.speed = msg.twist.twist.linear.x 
#        if self.speed == 0:
#            self.light_brake_used = False
#            self.emergency_brake_active = False

    def scan_callback(self, scan_msg):
      # Obter os parâmetros do LiDAR
        angle_min = scan_msg.angle_min
        angle_inc = scan_msg.angle_increment
        max_angle = np.pi/8 #faixa de angulos que estou varrendo

        msg = AckermannDriveStamped()

        #limites aceitáveis para frenagem de emergencia
        TPB1 = 1.0         
        TFB = 0.8  

        min_ttc = float('inf')
#       iTTC = min_ttc


        # Immediately handle emergency brake state
#        if self.emergency_brake_active == 'True':
#            msg.drive.speed = 0.0
#            self.publisher_.publish(msg)
#            self.get_logger().info(f"Pubing: {msg.drive.speed :.2f}.")
#           return  # Skip further processing

        for i, r in enumerate(scan_msg.ranges):

            # i é o indice de iteração e r é o valor de distancia para o indice i.
            theta_i = angle_min + angle_inc * i 

            if abs(theta_i) > max_angle:
                continue

            dot_r = self.speed * np.cos(theta_i)
            # Só consideramos se o veículo está se aproximando do obstáculo
            if dot_r > 0:
                # Evita divisão por zero com max(-dot_r, 0.001)
                iTTC = r / max(dot_r, 0.001)
                
                if iTTC < min_ttc:
                    min_ttc = iTTC
                
        if min_ttc < TFB:
            # Frenagem de emergência: velocidade zero
#            self.emergency_brake_active = True
            msg.drive.speed = 0.0
            self.get_logger().info(f"[Emergency] Feixe {i} - iTTC: {min_ttc:.2f} s, frenagem total,reduzindo velocidade para {msg.drive.speed :.2f} m/s.")
            self.publisher_.publish(msg)
    
#        elif min_ttc < TPB1 and not self.light_brake_used: 
            # Frenagem leve: reduz velocidade para 70% da atual
#            msg.drive.speed = self.speed * 0.7
#            self.light_brake_used = True  # Marca que a frenagem leve já ocorreu
#            self.get_logger().info(f"[Light] Feixe {i} - iTTC: {iTTC:.2f} s, reduzindo velocidade para {msg.drive.speed :.2f} m/s.")
        
        


def main(args=None):
    rclpy.init(args=args)
    safety_node = SafetyNode()
    rclpy.spin(safety_node)
    safety_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()