## Geomesh
### A Python package for processing DEM data into georeferenced unstructured meshes using the [jigsaw-python](https://github.com/dengwirda/jigsaw-python) library.

#### Installation
The Jigsaw library must be initialized first by running `./setup.py install_jigsaw`, then, the package can be installed normally by doing `./setup.py install`:

```bash
./setup.py install_jigsaw # installs the Jigsaw C-library to the current Python environment
./setup.py install # Installs the geomesh library to the current Python environment
./setup.py develop # run this if you are a developer.
```
#### Requirements
* Python>=3.6
* CMake 
* C/C++ compilers