from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="imerit-ango",
    version="1.1.1",
    author="Faruk Karakaya",
    author_email="<faruk@ango.ai>",
    description="Ango-Hub SDK",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "python-socketio~=5.8.0",
        "APScheduler~=3.9.1",
        "websocket-client",
        "flask-socketio~=5.3.4",
        "requests~=2.27.1",
        "tqdm",
        "validators~=0.20.0",
        "boto3~=1.26.30",
    ],
    keywords=['imerit_ango', 'ango-hub', "imerit_ango sdk", "Ango", "Ango-hub"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
    ]
)
