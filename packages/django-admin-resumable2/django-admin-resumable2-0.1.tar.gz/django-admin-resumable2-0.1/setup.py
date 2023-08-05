import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'readme.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-admin-resumable2',
    version='0.1',
    packages=['admin_resumable2'],
    include_package_data=True,
    package_data={
        'admin_resumable2': [
            'templates/admin_resumable2/file_input.html',
            'static/admin_resumable2/js/resumable.js',
        ]
    },
    license='MIT License',
    description='A Django app for the uploading of large files from the django admin site.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/rjnp2/django-admin-resumable2',
    author='rjnp2',
    author_email='rjnp2@outlook.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.8",
    extras_require={
        "dev": ['twine>=4.0.2',]
    }
)
