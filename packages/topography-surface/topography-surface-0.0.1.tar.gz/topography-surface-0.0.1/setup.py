from setuptools import find_packages, setup

setup(
    name="topography-surface",
    packages=find_packages(),
    version='0.0.1',
    description='Exploring different approaches of determining roughness of a measured surface (reference object) by predicting phase in the centre of interferogram.',
    author='Daniel Jankowski',
    license='MIT',
    package_data={'': ['data/samples/noise/*.png', 'data/samples/raw/*.png']},
    include_package_data=True,
    install_requires=[
          'pandas',
          'numpy',
          'tqdm',
          "opencv-python",
          'Pillow'
      ],
)
