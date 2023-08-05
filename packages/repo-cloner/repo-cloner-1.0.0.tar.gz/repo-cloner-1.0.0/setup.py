import setuptools
import os
import re

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def load_version():
    """ Loads a file content """
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "src", "repo_cloner", "__init__.py"))
    with open(filename, "rt") as version_file:
        init_file = version_file.read()
        version = re.search(r"__version__ = '([0-9a-z.-]+)'", init_file).group(1)
        return version


setuptools.setup(name='repo-cloner',
                 version=load_version(),
                 description='Python utility for cloning repositories',
                 long_description=long_description,
                 author='Daniel Peczek',
                 author_email='danpeczek@gmail.com',
                 url='https://github.com/danpeczek/repo-cloner',
                 project_urls={
                     "Bug Tracker": "https://github.com/danpeczek/repo-cloner/issues",
                 },
                 # To provide executable scripts, use entry points in preference to the
                 # "scripts" keyword. Entry points provide cross-platform support and allow
                 # pip to create the appropriate form of executable for the target platform.
                 entry_points={
                     'console_scripts': [
                         'repo-cloner=repo_cloner.cloner:main'
                     ]
                 },
                 install_requires=["pyyaml"],
                 classifiers=[
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'Operating System :: POSIX',
                     'Programming Language :: Python',
                     'Topic :: Communications :: Email',
                     'Topic :: Software Development :: Bug Tracking'
                 ],
                 package_dir={"": "src"},
                 packages=setuptools.find_packages(where="src"),
                 python_requires=">=3.6"
                 )
