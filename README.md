# Lab 08: Intro to ROS 2 – Services & Conveyor Belt Simulation
**Course**: MXET 400 – Mechatronics II: Industrial Robotic Systems  
**Department**: Multidisciplinary Engineering Technology, Texas A&M University  

---

## 1. Overview & Objectives

In this lab, you transition from continuous data streams (Topics) to request-response communication (Services), and integrate ROS 2 services with physics simulation in Gazebo:
1. **Understand ROS 2 Services (`srv`)**: Learn the synchronous/asynchronous client-server architecture where a client sends a request and waits for a response from a server node.
2. **Explore Gazebo Simulation Services**: Query active simulation services and actuate a virtual industrial conveyor belt via `/CONVEYORPOWER`.
3. **Inspect Reference Implementations**: Understand `multiply_server.py` and `multiply_client.py` in `service_pkg`.
4. **Implement Addition Server & Client**: Write `addition_server.py` and `addition_client.py`, register their entry points in `setup.py`, and test communication.
5. **Integrate Services with Publishers**: Enhance `item_spawner.py` to spawn alternating colored blocks (red, blue, green), detect when they fall off the conveyor, delete them, and publish the current block color to the `/box_color` topic.

---

## 2. Package Architecture

This repository contains four integrated packages:
```text
lab08/
├── README.md                          # Lab instructions and command reference
├── service_pkg/                       # Task 2: Math service servers and clients
│   ├── package.xml
│   ├── setup.py                       # Console scripts entry points (students update in Task 2)
│   └── service_pkg/
│       ├── multiply_server.py         # Section 1: Multiplication server (Reference)
│       ├── multiply_client.py         # Section 1: Multiplication client (Reference)
│       ├── addition_server.py         # Section 2: Addition server (Student template)
│       └── addition_client.py         # Section 2: Addition client (Student template)
├── conveyorbelt_msgs/                 # Custom service definitions
│   └── srv/ConveyorBeltControl.srv    # Service definition: float64 power -> bool success
├── conveyorbelt_gazebo/               # Simulation environment & models
│   ├── launch/conveyorbelt.launch.py  # Gazebo Harmonic world launcher
│   ├── worlds/conveyorbelt.world      # Gazebo world file
│   └── urdf/                          # Box models (box.urdf, red_box.urdf, blue_box.urdf, green_box.urdf)
└── ros2_conveyorbelt/                 # Task 3: Conveyor belt plugin & spawner node
    ├── CMakeLists.txt
    ├── src/ros2gz_conveyorbelt_system.cpp
    └── python/
        ├── SpawnObject.py             # Single object spawner CLI tool
        └── item_spawner.py            # Automated alternating block spawner template
```

---

## 3. Prelab: Conveyor Belt Setup & Initial Test

### Step 1: Install Dependencies & Source Environment
Ensure you have the Gazebo ROS bridge packages installed:
```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

Source the ROS 2 Jazzy environment:
```bash
source /opt/ros/jazzy/setup.bash
```

### Step 2: Build the Workspace
Navigate to your workspace root, build, and source:
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```
*(Tip: If you have aliases configured: `go_ws` $\rightarrow$ `cd ~/ros2_ws`, `cb_all` $\rightarrow$ `colcon build --symlink-install`, `sros` $\rightarrow$ `source install/setup.bash`)*

### Step 3: Launch Simulation & Test Spawning
Open separate terminals to launch the world, spawn a test block, and run the belt:

#### Terminal 1 — Launch Gazebo:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch conveyorbelt_gazebo conveyorbelt.launch.py
```

#### Terminal 2 — Spawn a Single Block:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_conveyorbelt SpawnObject.py --package "conveyorbelt_gazebo" --urdf "box.urdf" --name "box" --x 0.0 --y -0.5 --z 0.76
```

#### Terminal 3 — Start and Stop Conveyor Belt:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash

# Start the conveyor belt (power: 40.0)
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 40.0}"

# Stop the conveyor belt (power: 0.0)
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 0.0}"
```

> [!NOTE]
> **Pre-Lab Checkoff**: Run the conveyor belt until the test block travels down the belt and falls off. Take a screenshot for your pre-lab report.

---

## 4. Task 1: Exploring ROS 2 Services

In this task, explore how services are exposed, inspect message signatures, and control the belt via the CLI.

### Step 1: List Active Services
With Gazebo running in Terminal 1, run the following in Terminal 3:
```bash
# List all active services
ros2 service list

# List services with their message types
ros2 service list -t
```
Look for `/CONVEYORPOWER` of type `[conveyorbelt_msgs/srv/ConveyorBeltControl]`.

### Step 2: Inspect Service Interface
Inspect the request and response structure of the conveyor service:
```bash
ros2 interface show conveyorbelt_msgs/srv/ConveyorBeltControl
```
Output:
```text
float64 power
---
bool success
```
* The top part (`float64 power`) represents the **Request**.
* The separator (`---`) divides request from response.
* The bottom part (`bool success`) represents the **Response**.

### Step 3: Call Service via CLI
Start the belt at power `40.0`, let it run, and then call it with `0.0` to stop:
```bash
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 40.0}"
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 0.0}"
```

---

## 5. Task 2: Creating a Service and Server (`service_pkg`)

### Section 1: Multiplication Server & Client (Reference)
Inspect the reference implementation in `service_pkg`:
* [`multiply_server.py`](file:///home/tony_bolt/ros2_ws/src/lab08/service_pkg/service_pkg/multiply_server.py): Hosts `/multiply_two_ints` using `example_interfaces/srv/AddTwoInts`. Computes `response.sum = request.a * request.b`.
* [`multiply_client.py`](file:///home/tony_bolt/ros2_ws/src/lab08/service_pkg/service_pkg/multiply_client.py): Sends integer requests `a` and `b` asynchronously and logs `response.sum`.

Inspect [`service_pkg/setup.py`](file:///home/tony_bolt/ros2_ws/src/lab08/service_pkg/setup.py) to see how entry points are registered under `console_scripts`:
```python
    entry_points={
        'console_scripts': [
            'multiply_server = service_pkg.multiply_server:main',
            'multiply_client = service_pkg.multiply_client:main',
        ],
    },
```

Test the reference multiplication nodes:

#### Terminal 1 — Multiplication Server:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg multiply_server
```

#### Terminal 2 — Multiplication Client:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run service_pkg multiply_client
```
*Enter two integers when prompted. Verify the result.*

---

### Section 2: Addition Server & Client (Student Implementation)

Using the multiplication nodes as a guide, complete the addition nodes:

1. **Complete [`addition_server.py`](file:///home/tony_bolt/ros2_ws/src/lab08/service_pkg/service_pkg/addition_server.py)**:
   * **Step 1**: Create the service server for `AddTwoInts` on service name `"add_two_ints"` with callback `self.callback_add_two_ints`.
   * **Step 2**: In `callback_add_two_ints(self, request, response)`, calculate `response.sum = request.a + request.b`.
   * **Step 3**: Log the request and response.
   * **Step 4**: Return the `response` object.

2. **Complete [`addition_client.py`](file:///home/tony_bolt/ros2_ws/src/lab08/service_pkg/service_pkg/addition_client.py)**:
   * **Step 1**: Create the client for `AddTwoInts` on service name `"add_two_ints"`.
   * **Step 2**: Create a request object: `request = AddTwoInts.Request()`, populate `request.a = a` and `request.b = b`.
   * **Step 3**: Send request asynchronously: `future = self.client.call_async(request)` and wait with `rclpy.spin_until_future_complete(self, future)`.
   * **Step 4**: Retrieve `response = future.result()` and log the sum.

3. **Register Entry Points in [`service_pkg/setup.py`](file:///home/tony_bolt/ros2_ws/src/lab08/service_pkg/setup.py)**:
   Add `addition_server` and `addition_client` to `console_scripts`:
   ```python
       entry_points={
           'console_scripts': [
               'multiply_server = service_pkg.multiply_server:main',
               'multiply_client = service_pkg.multiply_client:main',
               'addition_server = service_pkg.addition_server:main',
               'addition_client = service_pkg.addition_client:main',
           ],
       },
   ```

4. **Rebuild & Source**:
   ```bash
   cd ~/ros2_ws
   colcon build --symlink-install --packages-select service_pkg
   source install/setup.bash
   ```

5. **Run Addition Server & Client**:

   **Terminal 1**:
   ```bash
   source ~/ros2_ws/install/setup.bash
   ros2 run service_pkg addition_server
   ```

   **Terminal 2**:
   ```bash
   source ~/ros2_ws/install/setup.bash
   ros2 run service_pkg addition_client
   ```

---

## 6. Task 3: Integrating ROS Services with Publishers (`item_spawner.py`)

In this task, complete `item_spawner.py` so that blocks of alternating colors are spawned onto the conveyor, deleted when they reach the end, and their colors published to `/box_color`.

### Step 1: Complete `item_spawner.py`
Open [`ros2_conveyorbelt/python/item_spawner.py`](file:///home/tony_bolt/ros2_ws/src/lab08/ros2_conveyorbelt/python/item_spawner.py) and fill in the `# MODIFY HERE` sections:

1. **Import the message type** (around line 13):
   ```python
   from std_msgs.msg import String
   ```

2. **Initialize the publisher in `__init__`** (around line 40):
   ```python
   self.pub = self.create_publisher(String, 'box_color', 10)
   ```

3. **Cycle colors and publish in `spawn_object`** (around line 68):
   ```python
   # 1. Create a String message object
   color_msg = String()

   # 2. Assign color and advance self.col
   if self.col == 0:
       color_msg.data = "red"
       self.col = 1
   elif self.col == 1:
       color_msg.data = "blue"
       self.col = 2
   elif self.col == 2:
       color_msg.data = "green"
       self.col = 0

   # 3. Publish the color
   self.pub.publish(color_msg)
   ```

### Step 2: Run the Full System
Launch all three terminals to test your pipeline:

#### Terminal 1 — Gazebo Simulation:
```bash
source ~/ros2_ws/install/setup.bash
ros2 launch conveyorbelt_gazebo conveyorbelt.launch.py
```

#### Terminal 2 — Power Conveyor Belt:
```bash
source ~/ros2_ws/install/setup.bash
ros2 service call /CONVEYORPOWER conveyorbelt_msgs/srv/ConveyorBeltControl "{power: 15.0}"
```

#### Terminal 3 — Automated Item Spawner:
```bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_conveyorbelt item_spawner.py
```

#### Terminal 4 — Echo Block Color:
```bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /box_color
```

*Expected output in Terminal 4:*
```text
data: red
---
data: blue
---
data: green
---
```

---

## 7. Troubleshooting & Common Pitfalls

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| `No executable found` when running `addition_server` | Missing entry point in `setup.py` | Add `'addition_server = service_pkg.addition_server:main'` to `setup.py`, then run `colcon build` and `source install/setup.bash`. |
| `No executable found` when running `SpawnObject.py` | Missing execute permission | Run `chmod +x ~/ros2_ws/src/lab08/ros2_conveyorbelt/python/SpawnObject.py`, rebuild, and source. |
| `Environment variable 'AMENT_PREFIX_PATH' is not set` | Workspace not sourced | Run `source /opt/ros/jazzy/setup.bash` followed by `source ~/ros2_ws/install/setup.bash`. |
| Block doesn't move on the belt | Belt power is `0.0` or service not called | Call `/CONVEYORPOWER` with `{power: 15.0}` to `{power: 40.0}`. |
| Box is not deleted when falling | Gazebo dynamic pose not tracking | Ensure Gazebo simulation is unpaused and running in real time. |

---

## 8. Lab Questions & Report Deliverables

Address the following questions in your lab report:
1. **Topics vs. Services**: What is the key architectural difference between a Topic (`/box_color`) and a Service (`/CONVEYORPOWER`)? Why is a Service more appropriate for starting/stopping the conveyor belt or requesting a calculation, while a Topic is better for announcing the color of a block?
2. **Item Spawner Lifecycle**: Describe the logic loop in the `main()` function of `item_spawner.py`. How does the node continuously monitor the box position, know exactly when to delete an old box from Gazebo, and trigger the spawn of the next colored box?
3. **Screenshots Required**:
   * Pre-Lab checkoff: Block falling off the moving conveyor in Gazebo.
   * Task 2: Terminal output of `addition_server` and `addition_client` communicating.
   * Task 3: Split-screen view showing Gazebo running, the conveyor moving alternating colored blocks, and `ros2 topic echo /box_color` echoing `red`, `blue`, and `green`.
