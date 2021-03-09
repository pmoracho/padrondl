import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requirements = ['beautifulsoup4==4.6.0',
                        'requests==2.18.1',
                        'progressbar2==3.30.2']

setuptools.setup(
    name="padrondl", # Replace with your own username
    version="0.0.1",
    author="Patricio Moracho",
    author_email="pmoracho@gmail.com",
    description="Descarga de padrones del AFIP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmoracho/padrondl",
    packages=setuptools.find_packages(),
    package_data={
        'padrondl': ['padrondl.cfg'],
    },
    entry_points={
        'console_scripts': [
            'padrondl=padrondl.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities"
    ],
    python_requires='>=3.6',
    install_requires=install_requirements,
)
