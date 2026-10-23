#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AdditionClient(Node): # class name
    def __init__(self):
        super().__init__("add_two_ints_client") # node name

        # Step 1: Create the client
        self.client = self.create_client(
            # Service Type
            # Service name (like a radio station frequency, must be the same as server)
            )

        self.get_logger().info("Client node started!")
    
    def call_service(self, a, b):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for server...")
        
        # Step 2: Create the request (Use AddTwoInts.Request() to create a request object, then fill in the fields with the input integers)

        
        # Step 3: Send request and wait for response (modify to addition from multiply_client.py)

        
        # Step 4: Get and display the response (modify to addition from multiply_client.py)


def main(args=None):
    rclpy.init(args=args)
    node = AdditionClient()

    while True:
        try:
            a = int(input("Enter first integer (or -1 to quit): "))
            if a == -1:
                break
            b = int(input("Enter second integer: "))
            node.call_service(a, b)
        except ValueError:
            print("Please enter valid integers.")
    rclpy.shutdown()

if __name__ == "__main__":
    main()
