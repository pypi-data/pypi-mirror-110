from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='SNAKES_AND_LADDERS',
    version='1',
    packages=['SNAKES_AND_LADDERS'],
    url='https://github.com/GlobalCreativeCommunityFounder/SNAKES_AND_LADDERS',
    license='MIT',
    author='GlobalCreativeCommunityFounder',
    author_email='globalcreativecommunityfounder@gmail.com',
    description='This package contains implementation of the game "SNAKES_AND_LADDERS" on command line interface'
                ' with 100 tiles on the board.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "SNAKES_AND_LADDERS=SNAKES_AND_LADDERS.snakes_and_ladders:main",
        ]
    }
)