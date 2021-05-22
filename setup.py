from setuptools import find_packages, setup


with open('README.md') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    requirements = file.read().strip().split('\n')


setup(
    name='regex-peterhunt',
    author='Peter Hunt',
    author_email='huangtianhao@icloud.com',
    description='Clone of Hypixel Skyblock, but in Python Cmd.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/peter-hunt/skyblock',
    setup_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',

)
