import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='asp_lite',
    version='0.0.0',
    author='Lorenz Leutgeb',
    author_email='lorenz@leutgeb.xyz',
    description='A lightweight dialect for Answer Set Programming',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lorenzleutgeb/asp-lite',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': [
       'asp-lite     = asp_lite.cli:main_transpile',
       'asp-lite-fmt = asp_lite.cli:main_format',
    ]},
    install_requires=[
        'networkx>=2.1',
    ],
    license='MIT',
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
    ),
)
