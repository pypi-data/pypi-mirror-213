
from setuptools import setup, find_packages

setup(
    name='cloudservices',
    version='0.0.1',
    description='A sample Python project for rach pack',
    author='Rac',
    author_email='rachitmahajan6399@gmail.com',
    url='https://gitlab.com/bobble-public/backend/python-utils',
    packages=['cloudservices','cloudservices.storageservice','cloudservices.queueservice','cloudservices.config'],
    install_requires=['google-auth==2.17.3','google-cloud-pubsub==2.13.0','boto3==1.14.60','botocore==1.17.60','apache-libcloud==3.7.0','PyPubSub==4.0.3','pyparsing==3.0.9'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)