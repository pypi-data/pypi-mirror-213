from setuptools import setup, find_packages

VERSION = '0.1.3'
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
    install_requires=[],
    keywords='conversion',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)