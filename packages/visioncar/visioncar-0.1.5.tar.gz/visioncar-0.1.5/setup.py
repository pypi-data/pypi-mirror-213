import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='visioncar',
    author='VisionCar team',
    description='Python library for controlling ESP32 robot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['opencv-python', 'requests', 'zeroconf', 'simplejpeg'],
    entry_points={
        'console_scripts': [
            'visioncar=visioncar:__main__'
        ],
    },
)
