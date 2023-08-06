from setuptools import setup

setup(
    name='smartWebScraper',
    version='1.0.0',
    author='Dany Srour',
    author_email='dany.srour@gmail.com',
    description='A package that allows you to smartly scrape data from a web page and export it to a CSV file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danysrour/smartWebScraper',
    packages=['smartWebScraper'],
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
        'beautifulsoup4>=4.12.2',
        'python_dateutil>=2.8.2',
        'requests>=2.31.0',
    ],
    exclude_package_data={'': ['tests/*']},
)
