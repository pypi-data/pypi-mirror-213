from setuptools import setup, find_namespace_packages


def _read(f) -> bytes:
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="indexed-png-stats",
    description="Python library that inspects indexed PNG files.",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-datamining/indexed-png-stats",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    entry_points={
        "console_scripts": [
            "indexed-png-stats=indexed_png_stats.generate:sys_main",
        ]
    },
    version="0.0.1",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "pillow",
        "numpy",
    ]
)
