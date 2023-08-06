from setuptools import setup

setup(
    name='colorFinder',
    version='1.0.2',
    author='Dany Srour',
    author_email='dany.srour@gmail.com',
    description='A package for automatically finding the most common used colors in an image.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danysrour/imageColorFinder',
    packages=['colorFinder'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
            'Pillow',
            'requests',
        ],
    exclude_package_data={'': ['tests/*']},
)
