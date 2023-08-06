# A Python client for the OpenFlexure Microscope.  

The [OpenFlexure Microscope] is most often controlled by two pieces of software - the [OpenFlexure Microscope Server], which is written in Python and runs on the embedded Raspberry Pi, and [OpenFlexure Connect][Connect] which is a graphical interface written in Electron, that can be run either on the Raspberry Pi, or on another computer via a network connection.  However, if you want to write your own scripts to perform particular experiments or protocols, it's useful not to have to embed these into the the [OpenFlexure Microscope Server] or package them up as plugins.  This library exists to make it easy to control your microscope from a simple Python script that can run either on the Raspberry Pi, or over the network.  I particularly like to use it from a [Jupyter] notebook on my laptop, because it allows me to plot graphs and display images as I go.

## Installation

This module can be installed with ``pip install openflexure-microscope-client``, or by cloning the repository and running ``poetry install``.

## Usage

### Connect to your microscope
You can connect to the microscope either by specifying a hostname or IP address, or using mDNS.  If your network is relatively simple, and if you can see your microscope in the "nearby devices" section of [Connect], then mDNS is a zero-faff way of connecting to your microscope:
```python
import openflexure_microscope_client as ofm_client
microscope = ofm_client.find_first_microscope()
```
If your network is more complicated, or you know the address of your microscope, you can connect using the hostname or IP address.  By default, your microscope will declare itself as ``microscope.local`` though this also relies on mDNS so if the method above doesn't work, ``microscope.local`` may also not work.  
```python
microscope = ofm_client.MicroscopeClient("example.host.name")
```

### Check the connection
Usually, I run a few commands to check my microscope is working properly:
```python
pos = microscope.position
starting_pos = pos.copy()
pos['x'] += 100
microscope.move(pos)
assert microscope.position == pos
pos['x'] -= 100
microscope.move(pos)
assert microscope.position == starting_pos

# Check the microscope will autofocus
ret = microscope.autofocus()

# Acquire an image for sanity-checking too
image = microscope.grab_image()
f, ax = plt.subplots(1,1)
ax.imshow(np.array(image))
#print(image.metadata)
print("Active microscope extensions")
for k in microscope.extensions.keys():
    print(k)
```
After running this block, you should see a list of extensions that are currently active, and a picture taken by the microscope.  Given that we just autofocused, this image should be nice and sharp!

### Basic commands
There are a few basic commands built in as methods of the ``MicroscopeClient`` object:
  * ``position`` is a property that returns a dictionary with ``'x'``, ``'y'``, and ``'z'`` components, giving the position of the stage.
  * ``get_position_array()`` returns a 3-element ``numpy`` array with the same position in it.
  * ``move(position)`` accepts either a 3-element array or a dictionary as returned by ``position``, and performs an absolute move
  * ``move_rel(displacement)`` performs a relative move (i.e. supplying 0 will not move that axis)
  * ``capture_image()`` will take a new image from the camera and return it as a ``PIL`` image object
  * ``grab_image()`` will return the next image the camera sends in its MJPEG preview stream (i.e. it's quicker but lower quality than ``capture_image()``)
  * ``grab_image_array()`` returns the image as a ``numpy`` array.
  * ``autofocus()`` runs the fast autofocus routine, just like clicking the "autofocus" button in [Connect]

### Extensions
To run methods provided by the microscope extensions, you can use the ``extensions`` dictionary, to make ``get`` or ``post`` requests:
```python
microscope.extensions["your.extension.name"]["link_name"].get()
microscope.extensions["your.extension.name"]["link_name"].post_json({"key":"value"})
```

### Arguments and documentation
There is not currently much documentation beyond this README for the Python client.  However, the microscope API is pretty well documented.  This is the place to go to find out the details of what each command does, and what the arguments mean, particularly for any of the commands that take a `payload` argument; that's converted to JSON and passed directly to the corresponding HTTP POST request.  Currently, there is a static version of the API documentation linked from the [server readthedocs page], or you can access a live interactive version from `http://microscope.local:5000/api/v2/docs/swagger-ui`, replacing `microscope.local` with the IP or hostname of your microscope.

[server readthedocs page]: https://openflexure-microscope-software.readthedocs.io/en/master/api.html


## Development
### Installation
The dependencies are managed using poetry, so once you have cloned the repository, you can set up a virtual environment with ``poetry install``.

### Tests
There are some basic tests that can be run using ``pytest``.  This needs to be within the environment installed above, so use ``poetry run pytest``.  These mostly need to connect to a microscope; the easiest way to test this automatically is to build ``openflexure-microscope-server`` and run it locally - this will create a local dummy microscope server.  Some tests will be skipped because they need microscope hardware, but it should at least verify most of the URLs.  Running the tests requires you to have started that server already - it will not be started automatically.

[OpenFlexure Microscope]: https://openflexure.org/projects/microscope/
[Connect]: https://gitlab.com/openflexure/openflexure-connect
[OpenFlexure Microscope Server]: https://gitlab.com/openflexure/openflexure-microscope-server/
[Jupyter]: https://jupyter.org/