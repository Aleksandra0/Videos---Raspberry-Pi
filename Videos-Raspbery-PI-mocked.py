import subprocess
import time
#import RPi.GPIO as GPIO
import threading
import random

# Mocking the GPIO library if testing without Raspberry Pi
class MockGPIO:
    BOARD = "BOARD"
    IN = "IN"
    
    pin_states = {19: False, 21: False, 23: False}  # Initial pin states
    
    @staticmethod
    def setmode(mode):
        print(f"GPIO mode set to {mode}")
    
    @staticmethod
    def setup(pin, mode):
        print(f"Pin {pin} set up as {mode}")
    
    @staticmethod
    def input(pin):
        # Simulate reading the state of a pin (you can modify the state here)
        return MockGPIO.pin_states[pin]
    
    @staticmethod
    def set_pin_state(pin, state):
        # Manually change the pin state for testing
        MockGPIO.pin_states[pin] = state
    
    @staticmethod
    def cleanup():
        print("GPIO cleanup")

# Function to simulate random GPIO pin activations
def simulate_random_pin_activity(pins, duration):
    """
    Simulates random pin activity for a specified duration.
    
    :param pins: A list of pin numbers (e.g., [PIN_1, PIN_2, PIN_3])
    :param duration: Total time in seconds for which to run the simulation
    """
    start_time = time.time()

    while time.time() - start_time < duration:
        # Randomly decide how many pins to activate (0 to len(pins))
        num_pins_to_activate = random.randint(0, len(pins))

        # Randomly pick the pins to activate
        pins_to_activate = random.sample(pins, num_pins_to_activate)

        # Set the state of the selected pins to HIGH, and the others to LOW
        for pin in pins:
            if pin in pins_to_activate:
                GPIO.set_pin_state(pin, True)  # Simulate pin going HIGH
                print(f"Pin {pin} activated (HIGH)")
            else:
                GPIO.set_pin_state(pin, False)  # Simulate pin going LOW
                print(f"Pin {pin} deactivated (LOW)")

        # Wait for a random time between 1 and 50 seconds before changing the pin states again
        sleep_time = random.randint(1, 50)
        print(f"Waiting {sleep_time} seconds before the next pin state change...")
        time.sleep(sleep_time)


# Use MockGPIO when not running on a Raspberry Pi
GPIO = MockGPIO

# Declaration of Pin Values
PIN_1 = 19
PIN_2 = 21
PIN_3 = 23

# Seting the pin numbering mode to use the physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Setting PINS as an Inputs - To read the state of the pin.
GPIO.setup(PIN_1, GPIO.IN)
GPIO.setup(PIN_2, GPIO.IN)
GPIO.setup(PIN_3, GPIO.IN)

# Table with [pin, 'name_of_the_video', duration of video (in seconds)]
Videos = [
    [PIN_1, './PlikiVideo/1.mp4', 14],
    [PIN_2, './PlikiVideo/2.mp4', 22],
    [PIN_3, './PlikiVideo/3.mp4', 3]
]

#Start Video function (default)
def start_vlc(video_path, fullscreen=False, new_window=False):
    vlc_path = 'vlc'  # VLC is typically installed as 'vlc' in Linux, no need for a full path
    fullscreen_option = '--fullscreen' if fullscreen else ' '

    # Return subprocess to start VLC
    return subprocess.Popen([vlc_path, fullscreen_option, "--no-playlist-enqueue", "--no-video-title-show", "--intf", "dummy", "--no-qt-privacy-ask",'--no-video-deco', '--no-embedded-video', "--loop", video_path])
    
# Start the default video
default_video_path = './PlikiVideo/0.mp4'  # Path to the default video, change if needed 
print(f"Starting default video: {default_video_path}")
current_process = start_vlc(default_video_path, fullscreen=False)
current_video = default_video_path

# Simulate random pin activity for 5min 
pins = [PIN_1, PIN_2, PIN_3]
simulation_duration = 300  # Simulate for 5 minutes (300 seconds)

# Running the simulation in a separate thread
simulation_thread = threading.Thread(target=simulate_random_pin_activity, args=(pins, simulation_duration))
simulation_thread.start()

try:
   while True:
    for video in Videos:
        
        pin = video[0]
        video_name = video[1]
        video_duration = video[2]

        # Reading the state of a PIN
        pin_state = GPIO.input(pin)

        # Conditions to run new video (pin is active and current video is not the same as video assigned to this pin)
        if (pin_state == True and current_video != video_name):
            
            print(f"Switching to video: {video_name} (most recently activated pin: {pin})")

            # Start the new video
            new_process = start_vlc(video_name, fullscreen=False)

            # Terminate the current video process if it exists
            if current_process is not None:
                time.sleep(0.2)
                print(f"Terminating current video: {current_video}")
                current_process.terminate()

            # Update current process and video
            current_process = new_process
            current_video = video_name

            #wait until video is finished
            time.sleep(video_duration)

            #Check again if any pin is active - if not, play default video
            is_any_pin_active = False

            for video_p in Videos:
                pin_p = video_p[0]
                # Reading the state of a PIN
                pin_state_p = GPIO.input(pin)
                if pin_state_p == True:
                     is_any_pin_active = True

            if is_any_pin_active == False:
                print(f"Starting default video: {default_video_path}")

                # Terminate the current video process if it exists
                if current_process is not None:
                    time.sleep(0.2)
                    print(f"Terminating current video: {current_video}")
                    current_process.terminate()

                current_process = start_vlc(default_video_path, fullscreen=True)
                current_video = default_video_path
    
    time.sleep(0.1)  # Check the state of pins every 100ms


except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    if current_process is not None:
        print("Terminating the last video.")
        current_process.terminate()

