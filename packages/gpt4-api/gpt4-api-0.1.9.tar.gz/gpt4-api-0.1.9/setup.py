from setuptools import setup, find_packages
from __init__ import __version__
name = 'gpt4-api'
requires_list = open('requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [i.strip() for i in requires_list]
setup(
    name=name,
    version=__version__,
    description='gpt4 api engine',
    author='changjun.yuan',
    author_email='455255111@qq.com',
    packages=find_packages(),
    package_data={"": ["*"]},
    python_requires='>=3.7.0',
    include_package_data=True,
    install_requires=requires_list,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)

# python setup.py sdist bdist_wheel
# twine upload -r pypi  dist/* --verbose
