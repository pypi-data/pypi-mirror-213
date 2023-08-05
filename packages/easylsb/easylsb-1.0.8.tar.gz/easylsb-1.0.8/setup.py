from setuptools import setup
import sys
import os
req=["wave", "des", "numpy","chardet","rsa"]
if sys.version_info.major==3:
    req.append('pillow')
def readme():
    with open('README.md','r') as file:
        return file.read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
setup(
    name="easylsb",
    version="1.0.8",
    description="Simple Python package for steganography",
    long_description=readme(),
    long_description_content_type='text/markdown',
    py_modules=["lsb"],
    install_requires=req,
    entry_points={
        "console_scripts": [
            "lsb_image=lsb:_script_image",
            "lsb_audio=lsb:_script_audio",
        ]
    },
)
