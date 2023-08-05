from setuptools import setup
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cove_unified_logs',
    version='0.1.7',
    description='A Python logging library for unified logging across AWS Lambda, Django, and Google Cloud servers. Logs are asynchronously pushed to AWS CloudWatch.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Coveidentity Tech Private Limited',
    author_email='sarvpriye.soni@coveidentity.com',
    url='https://github.com/Cove-Identity/cove-unified-logs',
    packages=['cove_unified_logs'],
    install_requires=[
        'boto3',
        'python-json-logger',
        'redis',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
