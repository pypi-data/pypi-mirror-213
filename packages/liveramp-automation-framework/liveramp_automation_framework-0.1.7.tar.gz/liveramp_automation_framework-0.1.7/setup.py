from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='liveramp_automation_framework',
    version='0.1.7',
    author='Jasmine Qian',
    author_email='jasmine.qian@liveramp.com',
    description="This is the base liveramp_automation_framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LiveRamp/qe_api_framework",
    packages=['liveramp_automation'],
    install_requires=[
        'pytest',
        'pytest-bdd',
        'pytest-playwright',
        'allure-pytest-bdd',
        'allure-python-commons',
        'google',
        'google-api-core',
        'google-auth',
        'google-cloud-bigquery',
        'google-cloud-core',
        'google-cloud-storage',
        'google-crc32c',
        'google-resumable-media',
        'googleapis-common-protos',
        'PyYAML',
        'pytest-json-report',
        'pytest-json',
        'pytest-xdist',
        'requests',
        'selenium==4.8.3',
        'pytest-bdd==6.1.1',
        'PyYAML==6.0',
        'webdriver-manager==3.8.6',
        'retrying==1.3.4',
    ],
)
