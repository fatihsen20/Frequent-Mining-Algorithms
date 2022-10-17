import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='FIM_Project',
    author='Fatih SEN',
    version="0.0.3",
    author_email='fatih.sn2000@gmail.com',
    description='Example PyPI (Python Package Index) Package',
    keywords='example, pypi, package, FIM, Frequent Itemset Mining, Association Rule Mining',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fatihsen20/FIM',
    project_urls={
        'Documentation': 'https://github.com/fatihsen20/FIM',
        'Source Code': 'https://github.com/fatihsen20/FIM',
    },
    package_dir={'': 'FIM'},
    packages=setuptools.find_packages(where='FIM'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=['numpy'],
)