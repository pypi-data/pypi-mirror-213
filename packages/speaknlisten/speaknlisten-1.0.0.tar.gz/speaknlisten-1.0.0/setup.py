import pyttsx3
import speech_recognition as sr
import datetime
from setuptools import setup, find_packages

setup(
    name='speaknlisten',
    version='1.0.0',
    author='Gautam Yadav',
    author_email='gautamdiscoder@gmail.com',
    description='Can use to speak and listen.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gautamdis/voice',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
