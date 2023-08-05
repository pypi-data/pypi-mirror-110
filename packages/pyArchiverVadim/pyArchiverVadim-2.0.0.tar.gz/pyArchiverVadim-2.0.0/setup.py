import setuptools
import pyArchiver


with open('README.md') as fr:
    long_description = fr.read()


setuptools.setup(
    name='pyArchiverVadim',
    version=pyArchiver.__version__,
    author='Silenov V.O.',
    author_email='veeeedro@mail.ru',
    description='Archiver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/veeeedro/pyArchiver',
    packages=setuptools.find_packages(),
    install_requires=[],
    test_suite='tests',
    python_requires='>=3.7',
    platforms=["any"]
)