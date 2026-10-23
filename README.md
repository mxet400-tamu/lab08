# Lab 08: ROS 2 Services & Conveyor Belt Simulation
**Course**: MXET 400 – Mechatronics II: Industrial Robotic Systems  
**Department**: Multidisciplinary Engineering Technology, Texas A&M University  

---

## 1. Overview & Objectives

In this lab, you transition from asynchronous continuous data streaming (Topics) to synchronous request-response communication (Services), followed by integrating services into a Gazebo simulation:
1. **Understand ROS 2 Services (`srv`)**: Learn the client-server pattern where a client sends a request and waits for a specific response.
2. **Inspect Reference Multiplication Service**: Understand how service servers and client nodes communicate using standard interfaces (`example_interfaces/srv/AddTwoInts`).
3. **Implement Addition Service**: Build your own addition server and client nodes, update `setup.py` with the new entry points, and test communication.
4. **Simulate Industrial Conveyor Belt in Gazebo**: Actuate a moving conveyor belt via the `/CONVEYORPOWER` service.
5. **Dynamic Entity Spawning & Color Tracking**: Complete the `item_spawner.py` node to spawn alternating colored boxes (red, blue, green), detect when they drop off the belt, delete them, and publish the current block color to the `/box_color` topic.

---

## 2. Package Architecture

This repository contains four integrated packages:
```text
lab08/
├── README.md                          # Lab guide & command reference
├── service_pkg/                       # Task 2: Math service servers and clients
│   ├── package.xml
│   ├── setup.py                       # Console scripts entry points
│   └── service_pkg/
│       ├── multiply_server.py         # Reference server for /multiply_two_ints
│       ├── multiply_client.py         # Reference client for /multiply_two_ints
│       ├── addition_server.py         # Student template for /add_two_ints
│       └── addition_client.py         # Student template for /add_two_ints
├── conveyorbelt_msgs/                 # Service message definitions
│   └── srv/ConveyorBeltControl.srv    # Custom service definition (power float)
├── conveyorbelt_gazebo/               # Simulation environment & models
│   ├── launch/conveyorbelt.launch.py  # Gazebo world launcher
│   ├── worlds/conveyorbelt.world      # World containing the conveyor belt
│   └── urdf/                          # Box models (box, red_box, blue_box, green_box)
└── ros2_conveyorbelt/                 # Conveyor belt control plugin & spawner
    ├── src/ros2gz_conveyorbelt_system.cpp
    └── python/
        ├── SpawnObject.py             # Single object spawner CLI tool
        └── item_spawner.py            # Automated alternating spawner template
```

---

## 3. Getting Started & Workspace Build

Build all packages from the root of your workspace:

```bash
# 1. Navigate to workspace root
cd ~/ros2_ws

# 2. Build the packages
colcon build --symlink-install

# 3. Source the workspace
source install/setup.bash
```

> [!TIP]
> If you have shell aliases configured:
> - `go_ws` -> `cd ~/ros2_ws`
> - `cb_all` -> `colcon build --symlink-install`
> - `sros` -> `source install/setup.bash`

---

## 4. Lab Tasks & Execution Commands

### Prelab: Conveyor Belt Launch & Verification

#### Terminal 1 — Launch Gazebo Conveyor Belt:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch conveyorbelt_gazebo conveyorbelt.launch.py
```

#### Terminal 2 — Spawn Single Test Block:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_conveyorbelt SpawnObject.py --package "conveyorbelt_gazebo" --urdf "box.urdf" --name "box" --x 0.0 --y -0.5 --z 0.76
```

#### Terminal 3 — Control Conveyor Power:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

# Start conveyor belt (power: 40)
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 40}"

# Stop conveyor belt (power: 0)
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 0}"
```

---

### Task 1: Exploring ROS 2 Services

With Gazebo running in Terminal 1:

```bash
# List all active services
ros2 service list

# List active services with their interface types
ros2 service list -t

# Inspect the conveyor control service interface
ros2 interface show conveyorbelt_msgs/srv/ConveyorBeltControl
```

Test starting and stopping the belt via service calls as described in the lab manual.

---

### Task 2: Creating a Service and Server (`service_pkg`)

#### Section 1: Multiplication Service (Reference)
Inspect `multiply_server.py` and `multiply_client.py` in `service_pkg/service_pkg/`. Notice how `console_scripts` in `service_pkg/setup.py` exposes them as ROS 2 executables.

##### Terminal 1 — Run Multiplication Server:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg multiply_server
```

##### Terminal 2 — Run Multiplication Client:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg multiply_client
```

##### Testing via CLI:
```bash
ros2 service call /multiply_two_ints example_interfaces/srv/AddTwoInts "{a: 7, b: 9}"
```

---

#### Section 2: Addition Service (Student Implementation)
Using the multiplication code as a reference:
1. Open `addition_server.py` and `addition_client.py` and follow the `# Step` comments to implement the addition service.
2. Update `service_pkg/setup.py` by adding the entry points for `addition_server` and `addition_client` to `console_scripts`.
3. Rebuild and source:
   ```bash
   cd ~/ros2_ws
   colcon build --symlink-install --packages-select service_pkg
   source install/setup.bash
   ```

##### Terminal 1 — Run Addition Server:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg addition_server
```

##### Terminal 2 — Run Addition Client:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg addition_client
```

##### Testing via CLI:
```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 12, b: 18}"
```

---

### Task 3: Gazebo Conveyor Belt & Automated Item Spawner

In this task, complete `item_spawner.py` so that boxes of alternating colors spawn onto the belt, drop off, are automatically deleted, and have their colors published.

1. Follow the `# MODIFY HERE` instructions in `ros2_conveyorbelt/python/item_spawner.py` and Section 1 of Task 3 in the lab manual.
2. Rebuild and source:
   ```bash
   cd ~/ros2_ws
   colcon build --symlink-install
   source install/setup.bash
   ```

#### Run the 4-Terminal Pipeline:

##### Terminal 1 — Gazebo Simulation:
```bash
source ~/ros2_ws/install/setup.bash
ros2 launch conveyorbelt_gazebo conveyorbelt.launch.py
```

##### Terminal 2 — Power Conveyor Belt:
```bash
source ~/ros2_ws/install/setup.bash
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 15}"
```

##### Terminal 3 — Automated Spawner Node:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_conveyorbelt item_spawner.py
```

##### Terminal 4 — Echo Block Color:
```bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /box_color
```

---

## 5. Checkpoint Checklist & Report Deliverables

Before completing your lab report, verify:
* [ ] Multiplication server returns product to client and CLI calls.
* [ ] Addition server and client are registered in `setup.py` and return accurate sum.
* [ ] Conveyor belt starts and stops via `/CONVEYORPOWER` service calls.
* [ ] Red, blue, and green boxes spawn in order, travel down the belt, and are deleted when falling off ($z < 0.05$ m).
* [ ] `/box_color` echoes `red`, `blue`, `green` as each box is placed on the belt.
* [ ] Answer both Lab Questions from the manual in your report.
