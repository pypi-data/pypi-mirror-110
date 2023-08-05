import setuptools

with open('structlinks/README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='structlinks',
    version='1.1.2',
    author='Eeshan Narula',
    author_email='eeshannarula29@gmail.com',
    description='Easily access and visualize different Data structures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eeshannarula29/structlinks',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.0'
)
