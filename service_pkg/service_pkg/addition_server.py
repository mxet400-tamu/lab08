#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AdditionServer(Node):   # Class Name
    def __init__(self):
        super().__init__("add_two_ints_server") # Node Name
        
        # Step 1. Create the service server (service_type, service_name, callback function)
        self.server_ = self.create_service(
            # Service type
            # Service name (like a radio station frequency, must be the same as client)
            # Callback function
        )
        self.get_logger().info("Add Two Ints Server has been started!")

    # This function runs when a client makes a request
    def callback_add_two_ints(self, request, response):
        # Step 2. Calculate the sum of the two integers and store it in the response object
        # Step 3. Log the request and response
        # Step 4. Return the response object
        pass

def main(args=None):
    rclpy.init(args=args)
    node = AdditionServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
