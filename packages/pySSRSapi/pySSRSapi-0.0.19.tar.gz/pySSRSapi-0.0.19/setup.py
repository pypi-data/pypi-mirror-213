from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pySSRSapi',
    version='0.0.19',
    description='Python SSRS API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='SSRS, API',
    author='quaik8',
    author_email='mail@example.com',
    url='https://pypi.org/project/pySSRSapi/',
    python_requires='>=3.7',
    packages=['pySSRSapi'],
    install_requires=['requests'],
    license="MIT license",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7'
    ]
)