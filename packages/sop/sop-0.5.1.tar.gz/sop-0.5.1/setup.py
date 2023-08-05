import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('sop/__version__.py', 'r') as fh:
    version = fh.read().split("'")[1]

setuptools.setup(
    name='sop',
    version=version,
    author='Daniel Kahn Gillmor',
    author_email='dkg@fifthhorseman.net',
    description='A framework for implementing the Stateless OpenPGP CLI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/dkg/python-sop',
    package_data={"sop": ["py.typed"]},
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
    ],
    python_requires='>=3.7',
)
