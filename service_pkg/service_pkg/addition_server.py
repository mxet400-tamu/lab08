#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsServerNode(Node):
    def __init__(self):
        super().__init__("add_two_ints_server")
        
        # Create service server
        self.server_ = self.create_service(
            AddTwoInts,              # Service type
            "add_two_ints",          # Service name
            self.callback_add_two_ints  # Callback function
        )
        
        self.get_logger().info("Add Two Ints Server has been started!")
    
    def callback_add_two_ints(self, request, response):
        # This function runs when a client makes a request
        response.sum = request.a + request.b
        self.get_logger().info(f"{request.a} + {request.b} = {response.sum}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

