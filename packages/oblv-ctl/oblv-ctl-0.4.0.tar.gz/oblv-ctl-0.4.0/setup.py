import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='oblv-ctl',
    version='0.4.0',
    description='A client library for accessing Oblivious APIs',
    author='Oblivious Support',
    author_email='support@oblivious.ai',
    license='Apache-2.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ObliviousAI/oblv-ctl',
    keywords=['Oblivious', 'python', 'package'],
    packages=find_packages(),
    install_requires=[
        'httpx==0.15.0',
        'python-dateutil==2.8.2',
        'typer==0.7.0',
        'rich~=11.1',
        'requests==2.29.0',
        'check-jsonschema==0.22.0',
    ],
    entry_points={
        'console_scripts': [
            'oblv-ctl=oblv_ctl.cli.main:app',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    package_data={"oblv_ctl": ["py.typed"]},
)