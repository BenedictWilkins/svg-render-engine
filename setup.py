from setuptools import setup, find_packages

setup(
    name="svgrenderengine",
    version="0.1.0",
    author="Benedict Wilkins",
    author_email="benrjw@@gmail.com",
    description="An SVG image renderer that allows for run-time manipulation, animation and user input capture.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "uuid",
        "cairosvg",
        "jinja2",
        "lxml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
