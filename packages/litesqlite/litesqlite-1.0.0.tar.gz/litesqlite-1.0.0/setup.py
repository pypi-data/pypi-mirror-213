from setuptools import setup

setup(
    name='litesqlite',
    version='1.0.0',
    description='Convenient work with sqlite3 and aiosqlite',
    url='https://github.com/FREVOD/litesqlite',
    author='FREVOD',
    author_email='frevod_dev@mail.ru',
    license='GPLv3',
    packages=['litesqlite'],
    install_requires=[
        'aiosqlite'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)