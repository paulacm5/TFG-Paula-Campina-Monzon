
El código original puede descargarse de: https://github.com/icisneros/cs182_finalproject_ICJH
El código implementado en el proyecto Localización de una plataforma móvil basada en LiDAR 2D y señales WiFi está dividido en tres carpetas:
1. Sensor --> contiene el archivo para la captación de datos.
2. Odometría+ICP --> contiene los siguientes ficheros:
			- conv_to_bin_mat.py
			- TrueMap.py
			- visualization_O.py
			- Odometry_O.py
			- Sensor_O.py
			- Robot_O.py
			
3. Particle Filter --> contiene los siguientes ficheros:
			- conv_to_bin_mat.py
			- TrueMap.py
			- visualization_L.py
			- ParticleFiler_L.py
			- Sensor_O.py
			- Sensor_L.py
			- Robot_L.py

El código usa las siguientes librerías (deben instalarse con: python -m pip install --upgrade xxx)
- matplotlib
- numpy
- scpy.misc
- pillow
- imageio

Para lanzar el código (Robot_L / Robot_O) se debe hacer desde la terminal de la Raspberry Pi.


En las carpetas SourceMaps y BinaryMaps se incluyen los planos de la planta 5 del edificio A de la EEBE.