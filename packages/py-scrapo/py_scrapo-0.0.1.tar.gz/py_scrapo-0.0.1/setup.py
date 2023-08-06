import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

__version__ = '0.0.1'

REPO_NAME = 'Flipkart_Webscrapping'
AUTHOR_USER_NAME = 'Mohsin Shaikh'
SRC_REPO = 'py_scrapo'
AUTHOR_EMAIL = 'mohsin.shaikh324@gmail.com'

setuptools.setup(
    name = 'py_scrapo',
    version = __version__,
    author = 'Mohsin Shaikh',
    author_email = AUTHOR_EMAIL,
    description = REPO_NAME,
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    python_requires='>=3.8',
    py_module = ['py_scrapo'],
    project_urls = {
        "Bug tracker":f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues'
        },
    package_dir = {"":"src"},
    packages = setuptools.find_packages(),
    keywords=['webscraper', 'flipkart', 'scrap'],
    install_requires = ['beautifulsoup4',
                        'requests',
                        'pandas',
                        'lxml']
)