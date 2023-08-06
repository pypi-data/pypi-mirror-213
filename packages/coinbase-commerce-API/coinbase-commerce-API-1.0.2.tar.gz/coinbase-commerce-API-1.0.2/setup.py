from setuptools import setup

setup(
    name='coinbase-commerce-API',
    version='1.0.2',
    author='Rushifakami',
    description='Unofficial Coinbase Commerce API library. See github for explanations and examples: https://github.com/Rushifakami/API-Coinbase-Commerce-cbc_api',
    packages=['cbc_api'],
    install_requires=[
        'requests',
    ],
    url='https://github.com/Rushifakami/API-Coinbase-Commerce-cbc_api',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
