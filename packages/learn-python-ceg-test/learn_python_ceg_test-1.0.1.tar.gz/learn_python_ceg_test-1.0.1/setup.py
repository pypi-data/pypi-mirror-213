import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='learn_python_ceg_test',                           # should match the package folder
    packages=['learn_python_ceg_test'],                   # should match the package folder
    version='1.0.1',                              # important for updates
    license='GNU',                                  # should match your chosen license
    description='learn_python check answers',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Miguel Angel Mendoza-Lugo, Robert Lanzafame, Ahmed Farahat',
    author_email='mendozalugo@gmail.com',
    url='https://github.com/mike-mendoza/learn_python_ceg_test', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/mike-mendoza/learn_python_ceg_test/issues"
    },
    install_requires=[ 'pandas'],    # list all packages that your package uses
    keywords=["pypi"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
    download_url="https://github.com/mike-mendoza/learn_python_ceg_test/archive/refs/tags/v1.0.1.tar.gz",
)