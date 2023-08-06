<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

### This package should be built AND installed in Windows

To build this package, you need:

1. Python>=3.6
2. pybind11 already installed in Python environment.

If you just want to install (using wheel), then pybind11 is not required.

Example code:

```python
from mciplayer import MCIPlayer
player=MCIPlayer() # Create a player instance, this will also create a MCI window.
player.open('test.wav') # Open the audio file
player.play() # Play the audio
player.wait() # Wait until the audio ends.
```

UTF-8 support has been added.