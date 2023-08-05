# This file is placed in the Public Domain.
#
# pylint: disable=W0012,C0114,C0116,W1514
# pylama: disable=E231


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(path):
    upl = []
    for file in os.listdir(path):
        if not file or file.startswith('.'):
            continue
        path2 = path + os.sep + file
        if os.path.isdir(path2):
            upl.extend(uploadlist(path2))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(path2)
    return upl


setup(
    name='genocide',
    version='120',
    url='https://github.com/thatebhj/genocide',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="Reconsider OTP-CR-117/19",
    long_description=read(),
    long_description_content_type='text/x-rst',
    license='Public Domain',
    packages=["genocide", "genocide.modules"],
    zip_safe=True,
    include_package_data=True,
    data_files=[
                ("genocde", [
                             "README.rst",
                             "MANUAL.rst"
                            ]
                ),
                ("share/doc/genocide", uploadlist("docs")),
                ("share/doc/genocide/pdf", uploadlist("docs/pdf")),
                ("share/doc/genocide/_static", uploadlist("docs/_static")),
                ("share/doc/genocide/_templates", uploadlist("docs/_templates")),
               ],
    scripts=[
             "bin/genocide",
            ],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
