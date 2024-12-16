# Stereoscopic Visualization with Smartphone HMD with Paraview and trame

This project showcases how to create a stereoscopic 3D visualization system using a smartphone as a Head-Mounted Display (HMD) in a web application built with **ParaView** and **trame**. It allows users to interact with 3D models in real-time by controlling the camera view with device orientation (e.g., tilting or rotating the phone). This is a university project for the course **Virtual Reality and Visualization**.

## Project Overview

The goal of this project is to enable immersive 3D visualization through simple devices, such as smartphones, by leveraging **ParaView** and **trame**. The smartphone acts as an HMD, allowing users to control the viewpoint of a 3D model by moving the device, without requiring specialized hardware like VR headsets.

### Key Features
- **Stereoscopic 3D rendering** in a web-based application.
- **Device motion control**: Use your smartphone’s accelerometer and gyroscope for camera orientation.

## Technologies Used

- **trame**: A Python framework used to build interactive web applications that connect to ParaView.
- **ParaViewWeb**: A web-based front-end to visualize 3D datasets.
- **Vuetify**: A Material Design framework for Vue.js, used for the front-end UI.
- **Device Orientation API**: A JavaScript API to capture orientation data from mobile devices for controlling the camera.

## How It Works

1. **ParaView** is used to generate 3D visualizations from data and export them for use in the web interface.
2. **Trame** is employed to stream the visualizations to the web and handle user interactions.
3. The smartphone's **device orientation** is captured via JavaScript and updates the camera's position in the 3D scene based on the device's movements.


## Getting Started

### Requirements
- **Python 3.9** (preferred version)
- **ParaView 5.10.1**

### Setup Instructions

1. **Clone the repository**:
   ```bash
   https://github.com/bkucharz/vrav-stereoscopic-view.git
   cd vrav-stereoscopic-view

2. Create a virtual environment:
    ```bash
    python3.9 -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    .\.venv\Scripts\activate  # Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

5. Start the Trame server: Run the Trame application script:
    ```bash
    .../ParaView-5.10.1.app/Contents/bin/pvpython \
    ./stereo_view.py  \
    --venv .venv

6. Open your browser at http://localhost:8080.

### Running on a Mobile Device (Local Network)

To access the application on your smartphone within the same local network:

1. Find your computer's local IP address:

    - On Windows: Run ipconfig in the command prompt and find the "IPv4 Address" under your network adapter.

    - On macOS/Linux: Run ifconfig or ip a in the terminal and find the IP address under your active network adapter.

2. Run the Trame server on your computer as described above.

3. Access the app on your phone:

    - Open a web browser on your smartphone.
    - Type in the local IP address of your computer followed by port 8080. For example, if your computer's IP is 192.168.1.100, you would enter: http://192.168.1.100:8080.
    - Ensure both your computer and smartphone are connected to the same Wi-Fi network.