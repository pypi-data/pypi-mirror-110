from setuptools import setup, find_packages

VERSION = '0.1.3'
DESCRIPTION = 'a small library that notifies you of a new word and its meaning every time you run it'
LONG_DESCRIPTION = 'You can customize it a little bit by using task shedular so that you can get to learn a new word (every let`s say one hour)'

# Setting up
setup(
    name="notifyVocab",
    version=VERSION,
    author="Mohammad Tayyib",
    author_email="tayyibsofi@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['PyDictionary', 'plyer'],
    keywords=['python', 'random-words', 'vocab', 'vocabulary', 'notification'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)