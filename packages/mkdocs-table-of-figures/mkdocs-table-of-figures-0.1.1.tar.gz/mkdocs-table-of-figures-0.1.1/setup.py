import io

from setuptools import setup, find_packages

setup(
    name='mkdocs-table-of-figures',
    version='0.1.1',
    description='A MkDocs plugin listing all figures to create a table of figures page',
    long_description=io.open('readme.md', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    keywords='mkdocs',
    url='https://gitlab.com/cfpt-mkdocs-plugins/mkdocs-table-of-figures',
    author='Thibaud Briard',
    author_email='thibaud.brrd@eduge.ch',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'mkdocs>=1.4.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.plugins': [
            'table-of-figures = mkdocs_table_of_figures.plugin:TableOfFigures'
        ]
    }
)