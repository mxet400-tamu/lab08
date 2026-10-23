#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClientNode(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")

        # Step 1: Create the client
        self.client = self.create_client(
            AddTwoInts, # client type
            "add_two_ints" # client name
            )

        self.get_logger().info("Client node started!")
    
    def call_service(self, a, b):
        # Step 2: Wait for server to be ready
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for server...")
        
        # Step 3: Create the request (like filling out an order form)
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        
        # Step 4: Send request and wait for response
        self.get_logger().info(f"Sending request: {a} + {b}")
        future = self.client.call_async(request)     # Return a future object like a buzzer that will go off when the response is ready or tracking info for a package delivery
        rclpy.spin_until_future_complete(self, future)
        
        # Step 5: Get and display the response
        response = future.result()              # without async, this would block the program until the response is received, but with async we can do other things while waiting for the response
        self.get_logger().info(f"Result: {a} + {b} = {response.sum}")

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClientNode()

    while True:
        try:
            a= int(input("Enter first integer (or -1 to quit): "))
            if a == -1:
                break
            b= int(input("Enter second integer: "))
            node.call_service(a, b)
        except ValueError:
            print("Please enter valid integers.")
    rclpy.shutdown()

if __name__ == "__main__":
    main()

