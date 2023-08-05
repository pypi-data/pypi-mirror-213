from setuptools import  setup, find_packages


setup(
    name='aistock',
    version="1.0.0",
    description='A tool for China stocks including stock data collection now and analysis in future.',
#     long_description=read("READM.rst"),
    long_description ="To be continued",
    author='dataat',
    author_email='btdan@sina.cn',
    license='BSD',
    url='http://dataat.top',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    keywords='Global Financial Data',
)