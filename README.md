# 3DVectorPython
A simple 3D vector rendering program made in python.
The user selects a 3D model and it renders a series of images that can be used to generate a GIF image. I made it for educational purposes only.

## Usage:
`main.py [filename.obj] [Nº images] [resolution X] [resolution Y]`

**Example:** `python main.py cube.obj 100 512 512`
*Renders 100 images of cube.obj with resolution 512x512*

**The images can be found in ImgBuffer folder**

Some parameters can be changed inside main.py and screen_draw.py.
**main.py parameters:**
- Translation and Rotation: **objRot** and **objPos** variables
- Color of the object: **objColor** variable
- Light direction: **lightDir** variable
- Field of view angle: **fFov** variable
- Render wireframe: **wireframe** variable (This one is pretty obvious)

**screen_draw.py parameters:**
- Background color: **bkgColor** variable

There are some other stuff inside that can be tweaked, feel free to explore and modify the code and maybe improve it in any way you like.
Some of those features are a bit broken for now and there are some noticiable bugs and glitches.

![alt text](https://github.com/JoaoPito/3DVectorPython/blob/master/GIFs/2405_cubeY_20fps.gif?raw=true)
![alt text](https://github.com/JoaoPito/3DVectorPython/blob/master/GIFs/2505_icoSphere_LoPoly2.gif?raw=true)
![alt text](https://github.com/JoaoPito/3DVectorPython/blob/master/GIFs/2705_cube_HQ.gif?raw=true)
*Here you can see that there are some serious glitches that need to be fixed*

