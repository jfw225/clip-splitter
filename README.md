# clip-splitter
 
Tool to quickly split a video into individual clips.

## Setup environment

Use your preferred package manager to install the packages listed in `requirements.txt`.

Using pip:

    $ python -m pip install -r requirements.txt

## Basic Usage

Run the tool inside the package directory:

    $ python main.py

After doing so, you will be promped to provide a path to a video. You can do so by typing the path, or by simply dragging the video into the prompt.

You can use these keyboard inputs to control the tool:

### SPACE BAR -> TOGGLE PLAYBACK

### ENTER/RETURN -> TOGGLE CLIP (first press starts clip, second saves clip)

### RIGHT/LEFT ARROW KEYS -> FORWARD/BACKWARD IN FRAMES

### UP/DOWN ARROW KEYS -> INCREASE/DECREASE PLAYBACK SPEED

### ESC -> EXIT TOOL

The console will output the current frame and speed.