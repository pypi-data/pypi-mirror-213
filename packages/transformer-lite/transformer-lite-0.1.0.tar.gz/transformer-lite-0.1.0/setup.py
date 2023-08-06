from setuptools import setup
setup(
    name='transformer-lite',
    version='0.1.0',
    author='Justinas Karaliunas',
    author_email='justinas@lorjus.com',
    description='A tiny library to do basic data transformations',
    long_description='A tiny library to do basic data transformations on tensors, time series & convolute',
    long_description_content_type='text/markdown',
    url='https://github.com/drootf/transformer-lite',
    packages=['transformer_lite'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
)