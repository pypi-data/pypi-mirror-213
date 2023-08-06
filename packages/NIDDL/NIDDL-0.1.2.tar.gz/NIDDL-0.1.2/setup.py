from setuptools import setup, find_packages

VERSION = '0.1.2'
DESCRIPTION = 'Neuro Imaging Denoising via Deep Learning (NIDDL)'
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
# LONG_DESCRIPTION = 'NIDDL code for denoising of volumetric calcium imaging recordings. \
#         If you find our code useful please cite \
#         Chaudhary, S., Moon, S. & Lu, H. Fast, efficient, and accurate neuro-imaging denoising via supervised deep learning. Nat Commun 13, 5165 (2022). https://doi.org/10.1038/s41467-022-32886-w'

setup(
    name="NIDDL",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Shivesh Chaudhary",
    author_email="shiveshc@gmail.com",
    license='MIT',
    packages=find_packages(),
    url='https://github.com/shiveshc/whole-brain_DeepDenoising',
    install_requires=[
        'absl-py==0.11.0',
        'astor==0.8.1',
        'bleach==1.5.0',
        'certifi==2020.6.20',
        'cycler==0.10.0',
        'Cython==0.29.21',
        'decorator==4.4.2',
        'gast==0.4.0',
        'google-pasta==0.2.0',
        'grpcio==1.35.0',
        'h5py==2.10.0',
        'html5lib==0.9999999',
        'imagecodecs==2019.12.31',
        'imagecodecs-lite==2020.1.31',
        'imageio==2.9.0',
        'importlib-metadata==2.1.1',
        'Keras==2.0.8',
        'Keras-Applications==1.0.8',
        'Keras-Preprocessing==1.1.2',
        'kiwisolver==1.1.0',
        'Markdown==3.2.2',
        'matplotlib==3.0.3',
        'networkx==2.4',
        'numpy==1.16.6',
        'opencv-python==4.4.0.42',
        'Pillow==7.2.0',
        'protobuf==3.14.0',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'PyWavelets==1.1.1',
        'PyYAML==5.3.1',
        'scikit-image==0.15.0',
        'scipy==1.4.1',
        'six==1.15.0',
        'tensorflow-gpu==1.6.0',
        'termcolor==1.1.0',
        'tifffile==2019.7.26.2',
        'tqdm==4.61.2',
        'Werkzeug==1.0.1',
        'wrapt==1.12.1',
        'zipp==1.2.0',
    ],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)