from setuptools import setup, find_packages

if __name__ == '__main__':
    name = 'taichu-dataflow'

    requirements = ['boto==2.49.0']

    long_description = ''
    # with open('README.md', 'r') as f:
    #     long_description = f.read()

    setup(
        name=name,
        version='1.0.5',
        description='taichu serve is a tool for serving dataflow',
        long_description=long_description,
        author='taichu platform team',
        python_requires=">=3.6.0",
        url='',
        keywords='taichu',
        packages=find_packages(),
        install_requires=requirements,
        include_package_data=True,
        package_data={
            '': ['*.sh'],
        }
    )
