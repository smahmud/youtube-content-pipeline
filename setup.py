from setuptools import setup, find_packages

setup(
    name="youtube-content-pipeline",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "yt_dlp",
        "click",
        "moviepy",
    ],
    entry_points={
        "console_scripts": [
            "extract-audio=cli:main",
        ],
    },
    python_requires=">=3.8",
)