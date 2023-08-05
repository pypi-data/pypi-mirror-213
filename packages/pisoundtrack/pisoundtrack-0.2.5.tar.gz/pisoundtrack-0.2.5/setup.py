import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pisoundtrack",
    version="0.2.5",
    author="Ismael Raya",
    author_email="phornee@gmail.com",
    description="Raspberry Pi Sound tracking and influx output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Phornee/pisoundtrack",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.yml'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation"
    ],
    install_requires=[
        'config_yml>=0.3.1',
        'log_mgr>=0.0.2',
        'influxdb_wrapper>=0.0.5',
        'numpy>=1.21.5',
        'pyaudio==0.2.11'
    ],
    python_requires='>=3.6',
)