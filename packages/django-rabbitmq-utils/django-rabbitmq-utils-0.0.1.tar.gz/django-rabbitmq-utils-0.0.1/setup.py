from setuptools import setup, find_packages
import io
import re

with io.open("README.md") as f:
    description = f.read()

with io.open("__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='django-rabbitmq-utils',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pika',  # RabbitMQ client library
        'kombu',
        'requests',
        'Django',
    ],
    description='Enhance RabbitMQ services for a Python Django application',
    long_description=description,
    long_description_content_type="text/markdown",
    author='Soniya Sharma',
    author_email='sharmasoniya6868@email.com',
    url='https://github.com/Soniyasharma6868/django_rabbitmq_utils',
    license="MIT",
    project_urls={
        "Source": "https://github.com/Soniyasharma6868/django_rabbitmq_utils",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    python_requires=">=3",
)
