from setuptools import setup, find_packages

setup(
    name='colorclip',
    version='1.0.4',
    author='Bevlil',
    author_email='voidlillis@gmail.com', 
    packages=find_packages(),
    py_modules=['colorclip'],
    url='https://t.me/Onefinalhug',
    download_url='https://github.com/lillisfeb/colorclip',
    description='A Python color pack library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='color pack library,python terminal console',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
)
