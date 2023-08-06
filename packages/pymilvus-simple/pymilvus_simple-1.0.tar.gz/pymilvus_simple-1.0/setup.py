import setuptools

setuptools.setup(
    name='pymilvus_simple',
    version='1.0',
    description='Simple wrapper of pymilvus.',
    author='Filip Haltmayer',
    author_email='filip@zilliz.com',
    url='https://github.com/filip-halt/pymilvus_simple',
    license="Apache-2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "pymilvus==2.2.9",
    ],
    python_requires='>=3.7'
)