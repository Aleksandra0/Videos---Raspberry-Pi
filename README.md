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

  
