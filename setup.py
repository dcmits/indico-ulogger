from setuptools import setup, find_packages


setup(
    name='indicoulogger',
    version='0.1',
    author='Giorgio Pieretti',
    author_email='gpieretti@unog.ch',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'indico>=1.9.1'
    ],
    entry_points={'indico.plugins': {'indicoulogger = indicoulogger:IndicoUserLoggerPlugin'}}
)
