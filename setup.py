from setuptools import setup, find_packages


setup(
    name = "decorlib",
    version = "0.1.2",
    author = "Richard Antal Nagy",
    author_email="nagy.richard.antal@gmail.com",
    description="Python library with decorators for ease of development",
    license = "MIT",
    keywords = [ "decorator", "development", "library", "performance", "helper" ],
    url = "https://github.com/dubniczky/decorlib",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    include_package_data=True,
    python_requires='>=3.8',
    long_description_content_type='text/markdown',
    long_description="Python library with decorators for ease of development"
)