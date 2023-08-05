from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-loki',
    version='0.1.4',
    packages=['django_loki'],
    url='https://github.com/zepc007/django-loki',
    license='MIT',
    author='zepc007',
    author_email='zepc007@gmail.com',
    description='logging handler with loki for django',
    long_description_content_type="text/markdown",
    long_description=long_description,
    keywords=['python', 'loki', 'grafana', 'logging', 'metrics'],
    install_requires=[
        'requests',
        'pytz',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Environment :: Web Environment",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Development Status :: 3 - Alpha '
    ],
)
