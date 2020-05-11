from setuptools import setup

setup(
    name='portfel',
    version='0.1.0',
    description='Portfolio analysis tools',
    author='Vasily Kuznetsov',
    author_email='kvas.it@gmail.com',
    packages=[
        'portfel',
        'portfel.data',
        'portfel.data.loaders',
    ],
    install_requires=[
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'pf=portfel.__main__:main',
        ]
    },
    include_package_data=True,
    license='GPLv3',
    zip_safe=False,
)
