from setuptools import setup

setup(
    name='gen_func',
    version='1.0.1',
    author='Maria Mora Rivas',
    author_email='morarivas02@gmail.com',
    description='The purpose of this package is to use the openai api to generate the body of a function that '
                'performs some database action',
    packages=['gen_func'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords=['relational databases', 'openai', 'LLM', 'python'],
    install_requires=[
        'openai',
        'pandas',
        'requests'
    ]
)
