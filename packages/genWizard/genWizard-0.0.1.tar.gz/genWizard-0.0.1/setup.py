
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='genWizard',
    version='0.0.1',
    description='genWizard allows for versatile usage of openAI generation and prompting management.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/ykim336/genWizard',
    license='MIT',
    classifiers=classifiers,
    keywords='machine learning',
    author='Isaac Moon',
    author_email='ykim336@ucr.com',
    packages=find_packages(),
    install_requires=['openai']
)

