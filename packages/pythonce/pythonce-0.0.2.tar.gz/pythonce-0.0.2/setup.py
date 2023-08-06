from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Programming Language :: Python :: 3',
]

setup(
    name='pythonce',
    version='0.0.2',
    description='Python Library writen in C ',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='carlinhoshk',
    author_email='carlosmdohk@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='c',
    packages=find_packages(),
    install_requires=[
        ''
    ]
)