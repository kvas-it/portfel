import os
from setuptools import setup

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, 'r', encoding='utf-8') as f:
    readme_md = f.read()

setup(
    name='portfel',
    version='0.1.0',
    description='Portfolio analysis tools',
    long_description=readme_md,
    long_description_content_type='text/markdown',
    author='Vasily Kuznetsov',
    author_email='kvas.it@gmail.com',
    packages=[
        'portfel',
        'portfel.data',
        'portfel.data.loaders',
    ],
    install_requires=[
        'tabulate',
        'pandas',
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
