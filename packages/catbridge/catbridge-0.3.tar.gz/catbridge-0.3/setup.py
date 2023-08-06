from setuptools import setup, find_packages

setup(
    name="catbridge",
    version="0.3",
    packages=find_packages(),

    # Metadata
    author="Bowen Yang",
    author_email="by172@georgetown.edu",
    description="A package for bridging cats",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    url="http://example.com/catbridge",  # Optional
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],

    install_requires=[
        # List your package's dependencies here
    ],
)
