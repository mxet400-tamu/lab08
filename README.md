# Lab 08: ROS 2 Services & Conveyor Belt Simulation
**Course**: MXET 400 – Mechatronics II: Industrial Robotic Systems  
**Department**: Multidisciplinary Engineering Technology, Texas A&M University  

---

## 1. Overview & Objectives

In this lab, you transition from continuous data streaming (Topics) to request-response communication (Services), followed by integrating services into a Gazebo simulation:
1. **Understand ROS 2 Services (`srv`)**: Learn the client-server pattern where a client sends a request and waits for a specific response.
2. **Build Multiplication and Addition Services**: Explore reference multiplication nodes and implement addition service nodes using standard interfaces (`example_interfaces/srv/AddTwoInts`).
3. **Simulate Industrial Conveyor Belt in Gazebo**: Use Gazebo plugins and ROS 2 services to actuate a moving conveyor belt (`/CONVEYORPOWER`).
4. **Dynamic Entity Spawning & Color Tracking**: Complete the spawner node to spawn colored boxes (red, blue, green) onto the conveyor belt, detect when they reach the end of the line, automatically delete them, and publish the current block color to a ROS 2 topic (`/box_color`).

---

## 2. Package Architecture

This repository contains four integrated packages:
```text
lab08/
├── README.md                          # This lab guide & command reference
├── service_pkg/                       # Math service servers and clients
│   ├── setup.py                       # Console scripts entry points
│   └── service_pkg/
│       ├── multiply_server.py         # Task 1: Reference server for /multiply_two_ints
│       ├── multiply_client.py         # Task 1: Reference client for /multiply_two_ints
│       ├── addition_server.py         # Task 2: Student template for /add_two_ints
│       └── addition_client.py         # Task 2: Student template for /add_two_ints
├── conveyorbelt_msgs/                 # Service message definitions
│   └── srv/ConveyorBeltControl.srv    # Custom service definition (power float)
├── conveyorbelt_gazebo/               # Simulation environment & models
│   ├── launch/conveyorbelt.launch.py  # Gazebo world launcher
│   ├── worlds/conveyorbelt.world      # World containing the conveyor belt
│   └── urdf/                          # Box models (box, red_box, blue_box, green_box)
└── ros2_conveyorbelt/                 # Conveyor belt control plugin & spawner
    ├── src/ros2gz_conveyorbelt_system.cpp
    └── python/
        ├── SpawnObject.py             # CLI object spawner tool
        └── item_spawner.py            # Task 3: Spawner node template with # MODIFY HERE
```

---

## 3. Getting Started & Workspace Build

Ensure you build all packages from the root of your workspace:

```bash
# 1. Navigate to workspace root
cd ~/ros2_ws

# 2. Build the packages
colcon build --symlink-install --packages-select conveyorbelt_msgs conveyorbelt_gazebo ros2_conveyorbelt service_pkg

# 3. Source the workspace
source install/setup.bash
```

*(Tip: If you have aliases configured: `go_ws` -> `cd ~/ros2_ws`, `cb_all` -> `colcon build --symlink-install`, `sros` -> `source install/setup.bash`)*

---

## 4. Lab Tasks & Execution Commands

### Task 1: Multiplication Service (Server & Client - Reference)

The multiplication server listens on service `/multiply_two_ints` and computes `a * b`. Review the code in `multiply_server.py` and `multiply_client.py` to see how a ROS 2 service client and server operate.

#### Terminal 1 (Run Multiplication Server):
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg multiply_server
```

#### Terminal 2 (Run Multiplication Client):
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg multiply_client
```

#### Terminal 3 (Testing via CLI):
You can also call the service directly from the command line without the client script:
```bash
ros2 service call /multiply_two_ints example_interfaces/srv/AddTwoInts "{a: 7, b: 9}"
```

---

### Task 2: Addition Service (Server & Client - Student Implementation)

Using the multiplication client and server as a reference, complete `addition_server.py` and `addition_client.py` in `service_pkg`. Add their entry points to `service_pkg/setup.py`, rebuild the package, and test your nodes:

#### Terminal 1 (Run Addition Server):
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg addition_server
```

#### Terminal 2 (Run Addition Client):
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg addition_client
```
*Enter two integers when prompted by the terminal.*

#### Terminal 3 (Testing via CLI):
```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 12, b: 18}"
```

---

### Task 3: Gazebo Conveyor Belt & Item Spawner Node

In this task, launch the conveyor simulation, power the belt via service, and complete `item_spawner.py` to publish the box color.

#### Step 1: Launch Gazebo Conveyor Belt
In **Terminal 1**:
```bash
source ~/ros2_ws/install/setup.bash
ros2 launch conveyorbelt_gazebo conveyorbelt.launch.py
```
*Gazebo will open displaying the conveyor belt on the virtual floor.*

#### Step 2: Power the Conveyor Belt via Service
In **Terminal 2**:
```bash
source ~/ros2_ws/install/setup.bash

# Check available conveyor services
ros2 service list | grep CONVEYOR

# Set belt power (e.g. 15.0 or 40.0)
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 15.0}"
```
*You will see the belt surface begin to move in Gazebo.*

#### Step 3: Complete `item_spawner.py`
Open `ros2_conveyorbelt/python/item_spawner.py` and follow the instructions in the `# MODIFY HERE` sections:
1. Import the appropriate message type for text and initialize the publisher on topic `/box_color`.
2. Add logic in `spawn_object()` to cycle through block colors (red, blue, green) and publish each color message.

#### Step 4: Run the Item Spawner Node
In **Terminal 3**:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_conveyorbelt item_spawner.py
```

#### Step 5: Verify Color Publishing
In **Terminal 4**:
```bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /box_color
```
*As each box spawns on the moving belt, drops off the end, and is deleted, you should see `/box_color` continuously echo the active block color.*

---

## 5. Checkpoint Checklist

Before completing your lab report, verify:
* [ ] Multiplication server returns accurate product to client and CLI calls.
* [ ] Addition server returns accurate sum to client and CLI calls.
* [ ] Conveyor belt moves when `/CONVEYORPOWER` is set to active power.
* [ ] Red, blue, and green boxes spawn in order, travel down the belt, and are deleted when falling off.
* [ ] `/box_color` echoes the matching color as each box is placed on the belt.
