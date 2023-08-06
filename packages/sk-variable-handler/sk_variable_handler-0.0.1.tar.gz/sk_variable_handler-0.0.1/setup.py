from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sk_variable_handler',
    version='0.0.1',
    description='A simple Variable Handling  program',
    author='gkibria',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type as Markdown
    author_email='gkibria121@gmail.com',
    packages=find_packages(),
    install_requires=['regex'],
    python_requires='>=3.6',
    keywords='python, report generator',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
