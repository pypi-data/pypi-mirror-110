from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []  # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="Brinson-api",
    version="1.0.1",
    description="Brinson module",
    author="lsd",
    author_email="",  # 作者的联系邮箱
    packages=find_packages(),
    # packages=["Brinson", ],
    install_requires=install_requires,
    include_package_data=True,
    long_description=long_description,  # 长描述，通常是readme，打包到PiPy需要
    long_description_content_type="text/markdown",  # 长描述文档类型
)

print("Welcome to download Brinson!")