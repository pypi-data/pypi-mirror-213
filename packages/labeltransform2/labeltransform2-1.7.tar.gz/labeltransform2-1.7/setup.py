import setuptools


setuptools.setup(
    name="labeltransform2",
    version="1.7",
    author="victor",
    description="dataset label style transform tool",
    url="https://gitee.com/free_bigD/labeltransform.git",
    packages=setuptools.find_packages(),
    install_requires=["opencv-python", "pandas"],
    python_requires='>=3'
)