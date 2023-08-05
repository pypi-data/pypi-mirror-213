# python setup.py sdist bdist_wheel  
# twine upload dist/*    

from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='openi-test',
    version='0.0.7',
    description='A test packages for openi pypi',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://openi.pcl.ac.cn/liuzx/openi-pypi-test',
    author='chenzh05,liuzx',
    author_email='chenzh.ds@outlook.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    install_requires=['emoji','requests','tqdm'],
    python_requires='>=3.6',
)