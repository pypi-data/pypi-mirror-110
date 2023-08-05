from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cfdp',
    version='1.0.2',
    author_email="info@librecube.org",
    description='CCSDS File Delivery Protocol',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/librecube/lib/python-cfdp",
    license='MIT',
    python_requires='>=3.4',
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    extras_require={
        'zmq': ['pyzmq']
    }
)
