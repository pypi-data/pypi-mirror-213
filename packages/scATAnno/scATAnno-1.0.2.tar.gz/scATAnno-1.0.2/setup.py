from setuptools import setup

setup(
    name='scATAnno',
    version='1.0.2',
    packages=['scATAnno'],
    url='https://github.com/aj088/scATAnno-main/',
    license='',
    author='Yijia Jiang',
    author_email='yijia_jiang@dfci.harvard.edu',
    description='',
    install_requires=['pandas','scanpy','anndata','matplotlib','adjustText', 'leidenalg', 'harmonypy', 'scipy','seaborn', "snapatac2"],
)
