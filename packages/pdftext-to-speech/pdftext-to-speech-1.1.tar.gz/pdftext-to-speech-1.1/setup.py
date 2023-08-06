from setuptools import setup, find_packages

setup(
    name='pdftext-to-speech',
    version='1.1',
    author='Dany Srour',
    author_email='dany.srour@gmail.com',
    description='A Python package for converting PDF and TXT files to audio',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danysrour/textToSpeech',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[
        'PyPDF2',
        'requests',
    ],
)
