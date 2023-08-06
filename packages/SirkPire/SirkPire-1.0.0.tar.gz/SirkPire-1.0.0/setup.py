from setuptools import setup, find_packages

setup(
    name = 'SirkPire',
    version = '1.0.0',
    author='MrTelepathic',
    author_email = 'shahrokhenhedam@gmail.com',
    description = 'This is a powerful and easy library for building self Bots in Rubika',
    keywords = ['rubika', 'rubika-bot', 'SirkPire', 'rubx', 'rubino', 'rubika.ir', 'bot','Rubipy'],
    long_description = open("README.md", encoding="utf-8").read(),
    python_requires="~=3.6",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/MrTelepathic/SirkPire',
    packages = find_packages(),
    install_requires = ['pycryptodome', 'websocket-client', 'requests', 'urllib3', 'pillow', 'mutagen', 'tinytag'],
    classifiers = [
    	"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ]
)
