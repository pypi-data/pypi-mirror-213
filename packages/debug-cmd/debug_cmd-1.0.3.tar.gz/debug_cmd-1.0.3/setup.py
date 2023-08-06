from os import path
from codecs import open
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='debug_cmd',
    packages=['debug_cmd'],
    version='1.0.3',
    license='MIT',
    install_requires=['openai'],
    author='Yusuke Kawatsu',
    author_email='mail@sample.com',
    url='https://github.com/megmogmog1965/debug_cmd',
    description='Debug linux command error by using GPT/LLM.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='gpt debug',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'debug_cmd=debug_cmd.debug_cmd:main',
        ],
    },
)
