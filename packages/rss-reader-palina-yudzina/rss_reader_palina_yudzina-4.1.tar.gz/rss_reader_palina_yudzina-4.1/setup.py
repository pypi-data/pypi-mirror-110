from setuptools import setup, find_packages
from os import path

directory = path.abspath(path.dirname(__file__))
with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="rss_reader_palina_yudzina",
    version="4.1",
    description="RSS reader - simple command-line utility.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PolinaYud/Final-Task",
    author="Polina Yudina",
    author_email="polina_yu@list.ru",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['feedparser', 'requests', 'beautifulsoup4==4.8.1', 'fpdf', 'dominate'],
    entry_points={
        'console_scripts':
            ['rss-reader = rss_reader_palina_yudzina.rss_reader:main']
    },
)
