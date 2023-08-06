from setuptools import setup, find_packages

setup(
    name='pdf_binder',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyPDF2',
        'Pillow',
        'pdf2image',
        'tqdm',
    ],
    entry_points={
        'console_scripts': [
            'create-signatures=pdf_binder.pdf_to_signatures:main',
        ],
    },
    author='Peter Herrmann',
    author_email='herrmannp7@gmail.com',
    description='A tool for preparing PDFs for bookbinding',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/Peter-Herrmann/pdf_binder',
)
