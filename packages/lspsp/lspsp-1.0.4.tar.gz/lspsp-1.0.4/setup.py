from setuptools import setup, find_packages

setup(
    name="lspsp",
    version="1.0.4",
    license='GPL',
    description='LSPSP.ME Monitor',
    long_description='LSPSP.ME Monitor Service',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'APScheduler==3.10.1',
        'beautifulsoup4==4.12.2',
        'Jinja2==3.1.1',
        'Requests==2.30.0',
        'setuptools==57.4.0',
    ],

    scripts=[],
    entry_points={
        'console_scripts': [
            'lspsp = lspsp.main:main'
        ]
    },
    data_files=[
        ('etc/lspsp', ['config.json.template'])
    ]
)
