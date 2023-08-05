from setuptools import find_packages, setup

setup(
    name='talos-python',
    version='3.0.0',
    author='huyume  i',
    author_email='huyumei@xiaomi.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cffi',
        'python-snappy',
        'atomic',
        'dnspython',
        'requests',
        'futures'
    ],
)

