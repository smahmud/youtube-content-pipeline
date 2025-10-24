from setuptools import setup, find_packages

setup(
    name="youtube-content-pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
    "pytubefix",
    "pydub",
    "ffmpeg-python",
    "click",
    ],
    entry_points={
        "console_scripts": [
            "extract-audio=clic:main",
        ],
    },
)