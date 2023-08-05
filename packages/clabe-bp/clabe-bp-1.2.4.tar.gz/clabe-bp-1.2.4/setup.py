from importlib.machinery import SourceFileLoader

import setuptools

version = SourceFileLoader('version', 'clabe/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='clabe-bp',
    version=version.__version__,
    author='BanPAY',
    author_email='dev@banpay.com',
    description='Validate and generate the control digit of a CLABE in Mexico',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lucf25/clabe-python',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data=dict(clabe=['py.typed']),
    install_requires=['pydantic>=1.4,<2.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
