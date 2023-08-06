from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='JenishVidjaPractical',
    version='0.0.1',
    description='A very basic pratcial file',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author = 'Jenish Vidja',
    author_email = '22bce123@nirmauni.ac.in',
    Lincense='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages = find_packages(),
    install_requires=['']

)
