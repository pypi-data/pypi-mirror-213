from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='multisesh',
    version='0.0.19',
    author='Tom Wyatt',
    author_email='womtyatt@gmail.com',
    url='https://github.com/TomPJWyatt/MultiSesh',
    license_files = 'MIT',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    description='For combining and analysing microscope imaging data made in multiple different sessions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'':'src'},
    packages=['multisesh'],
    install_requires=[
        'numpy>=1.14.5',
        'tifffile>=2020.11.18',
        'numpy>=1.19.4',
        'scipy>=1.5.3',
        'opencv-python>=4.5.0',
        'scikit-image==0.18.1',
        'scyjava',
        'matplotlib' 
    ]
)
