from setuptools import setup, find_packages
setup(
    name="network-tests",
    version="0.1",
    #packages=find_packages(),
    packages=['ping','bandwidth'],
    scripts=['ping/ping_test.py','bandwidth/download_speed.py','bandwidth/upload_speed.py','download-tester','upload-tester', 'ping-tester'],
    #scripts=['ping-test','download-speed','upload-speed'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['requests','numpy','pingparsing','statistics'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['hosts.txt'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author="Juan Luis Baptiste",
    author_email="juan.baptiste@gmail.com",
    description="Collection of scripts to do network tests like download/upload speeds, network latency (ping) and store results in a CSV file.",
    license="GPLv3",
    keywords="ping bandwidth download upload test",
    url="https://github.com/juanluisbaptiste/network-tests",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)
