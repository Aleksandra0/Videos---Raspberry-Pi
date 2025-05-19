# Videos---Raspberry-Pi
Simulation for a Raspberry Pi system that plays different videos depending on GPIO input signals.

## Features

- Simulates GPIO inputs to trigger different videos.
- Plays a default video when no input is active.
- Automatically switches to a new video when a pin is activated.
- Resumes default video playback after custom video finishes.
- Runs simulation in a separate thread using `threading`.
- Uses VLC player for media playback.
- Includes a mock GPIO class for testing without hardware.

## Technologies Used

- Python 3
- VLC Media Player (must be installed and available in system path)
- `subprocess`, `threading`, `time`, `random`
- (Optional) `RPi.GPIO` for actual Raspberry Pi usage

## How to run

1. **Open a terminal**
2. **Install VLC media player** using the following command:

   sudo snap install vlc
   
3. **Navigate to the directory containing the script:**

   cd ~/Your_Directory_Name
   
4. **Make sure Python 3 is installed:**

   python3 --version
   
5. **Run the Python script:**

   python3 your_script_name.py

6. **Stop the script with Ctrl + C (KeyboardInterrupt).**
   
