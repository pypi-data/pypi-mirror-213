from setuptools import setup

setup(
    name='PyMeas',
    version='0.1',
    description='This library has been developed specifically for the purpose of measuring parameters such as diameter, concentricity, and other relevant characteristics of ring-shaped components.',
    author='Mehmet Kaçmaz',
    author_email='mehmetkcmz5@gmail.com',
    packages=['pymeas'],
    install_requires=[
        'circle-fit',
        'opencv-python',
        'matplotlib',
        'pyodbc',
        'mpl_point_clicker',
        'subpixel-edges',
        'scikit-image'
    ],
)