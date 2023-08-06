from setuptools import setup, find_packages

# package info/config (use "pip install -e ." to instal locally for dev)
setup(
    name='modelbusinesscards',
    version='0.0.3',
    description='Generating documentation of AI model usage to increase visibility and safety',
    url='https://github.com/youmustfight/model-business-cards',
    package_dir={ '': 'src' }, # This tells setuptools to look for packages in the 'src' directory.
    packages=find_packages(where='src'), # find_packages() will find packages in the 'src' directory because of the above.
    install_requires=[],
    include_package_data=True,
    license='MIT',
    zip_safe=False
)
