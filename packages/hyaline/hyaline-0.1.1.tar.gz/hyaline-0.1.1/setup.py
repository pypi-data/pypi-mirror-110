from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='hyaline',
    version='0.1.1',
    description='Discord API Wrapper for Python!',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/5elenay/hyaline/',
    author='5elenay',
    author_email='',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/5elenay/hyaline/issues",
    },
    classifiers=classifiers,
    keywords=["discord", "wrapper", "api", "gateway", "lightweight", "discord-api"],
    packages=find_packages(),
    python_requires='>=3.6.0',
    install_requires=['python-dateutil', 'aiohttp']
)
