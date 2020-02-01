import subprocess
import os
import re

from pkg_resources import parse_version
from setuptools import setup, find_packages

name = 'cer'

with open('README.rst') as readme:
    README = readme.read()

stable_release = '0.0.1'


def git(*args):
    cmd = ['git'] + list(args)
    res = subprocess.check_output(cmd)
    return res[:-1]  # get rid of the newline


def write_init(version):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    init_path = os.path.join(this_dir, 'cer', '__init__.py')
    version_string = version
    parsed_version = parse_version(version)
    version_tuple = parsed_version._version.release
    if parsed_version._version.dev:
        version_tuple += parsed_version._version.dev
    if parsed_version._version.pre:
        version_tuple += parsed_version._version.pre
    if parsed_version._version.local:
        version_tuple += parsed_version._version.local
    version_file = "__version__ = '{}'\n\nVERSION = {}\n"
    version_file = version_file.format(version_string, version_tuple)
    with open(init_path, 'w') as f:
        f.write(version_file)


def get_version():
    try:
        # check if git is available
        git('status')
        # git is available so go to town
        version = stable_release + '+unknown'
        env = os.getenv("HEC_CER_ENVIRONMENT", None)
        if env == "PROD":
            version = stable_release
        elif env == "RELEASE":
            sha = git('rev-parse', 'HEAD')
            version = stable_release + 'rc0' + '+' + sha[:6]
        else:
            desc = str(git('describe').decode())
            msg = "Tag {} doesnt start with Stable {}"
            msg = msg.format(desc, stable_release)
            assert desc.startswith('v' + stable_release), msg
            match = re.match(r'^(.*)-([0-9]+)-g(.*)$', desc)
            if match:
                ver, distance, sha = match.groups()
                msg = "Tag {} is not equal to Stable {}"
                msg = msg.format(ver, stable_release)
                assert ver == 'v' + stable_release, msg
                version = stable_release + ".dev{}+{}".format(distance, sha)
        write_init(version)
    except (subprocess.CalledProcessError, OSError):
        # there's no git around, so this is probably
        # an installed package
        pass

    return __version__


setup(
    name=name,
    version=get_version(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    description='Vehicle recommendation app',
    long_description=open('README.rst').read(),
    url='',
    author='Sheriff',
    author_email='danmbugua74@gmail.com',
    license='Proprietary',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: All',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=[
        'gunicorn==19.7.1',
        'Click==6.7',
        'sarge==0.1.5',
        'ipython==6.2.0',
        'drfdocs==0.0.11',
        'ansible==2.6.2',
        'boto>=2.48.0',
    ],
    scripts=[
    ],
    include_package_data=True
)
