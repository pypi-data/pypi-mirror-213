from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='GILBypass',
    version='0.1.0',
    description='GILBypass (GILB) is a module that allows you to bypass the Global Interpreter Lock (GIL) in Python.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url='https://github.com/IHasBone/GILB',
    author='IHasBone',
    author_email='info@picstreme.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['GIL', 'bypass', 'GILBypass', 'GILB', 'global interpreter lock'],
    packages=find_packages(),
    python_requires='>=3.10'
)
