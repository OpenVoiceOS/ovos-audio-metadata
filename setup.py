#!/usr/bin/env python3
import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


setup(
    name="ovos-audio-metadata",
    version="0.12.0",
    description='metadata extractor from audio files',
    url='https://github.com/OpenVoiceOS/ovos-audio-metadata',
    author='thebigmunch',
    author_email='mail@thebigmunch.me',
    license='MIT',
    packages=["ovos_audio_metadata"],
    install_requires=required("requirements.txt"),
    package_data={'': package_files("ovos_audio_metadata")},
    zip_safe=True,
    include_package_data=True,
    keywords='ovos ocp'
)
