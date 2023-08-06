import setuptools


setuptools.setup(
    name="labeltransform2",
    version="1.2",
    author="victor",
    description="dataset label style transform tool",
    url="",
    packages=setuptools.find_packages(),
    install_requires=["opencv-python", "pandas"],
    python_requires='>=3'
)