from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='taichu-dataflow',
        version='1.0.0',
        description='taichu-dataflow is a tool for serving dataflow',
        long_description='',
        author='taichu platform team',
        # author_email='noreply@noreply.com',
        python_requires=">=3.6.0",
        url='',
        keywords='taichu',
        packages=find_packages(),
        install_requires=['boto==2.49.0'],
        include_package_data=True,
    )
