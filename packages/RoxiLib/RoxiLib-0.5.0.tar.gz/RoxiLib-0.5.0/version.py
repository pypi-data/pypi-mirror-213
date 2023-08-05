# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

__all__ = ("get_git_version")

from subprocess import Popen, PIPE
import re


def call_git_describe():
    try:
        p = Popen(['git', 'describe', '--tags'],
                  stdout=PIPE, stderr=PIPE)
        
        p.stderr.close()
        line = p.stdout.readlines()[0]
        stringValue = line.strip().decode('UTF-8')
        if stringValue.startswith('v'): #if using v prefixed tags, remove the v from here. 
            stringValue = stringValue.replace('v','')
        return str(stringValue)
    except Exception as e:
        print("Exception {0}".format(e))
        return None


def is_dirty():
    try:
        p = Popen(["git", "diff-index", "--name-only", "HEAD"],
                  stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        lines = p.stdout.readlines()
        return len(lines) > 0
    except Exception as e:
        print("Exception {0}".format(e))
        return False

def split_semantic_version(version):
    found = re.findall("^([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)\.([0-9]|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+)?$", version)
    if found:
        if len(found) == 1:
            return found[0]
    else:
        raise ValueError("Version not according to semantic versioning {0}".format(version))

def check_if_release(version):
    versionObj = split_semantic_version(version)
    if len(versionObj) > 3:
        if len(versionObj[3]) == 0: #it can be empty due to regex
            return 1
        else:
            return 0
    else:
        return 1

def update_to_dev_release(version):
    objects = split_semantic_version(version)
    print(objects)
    index=objects[3].index('-')
    devCount = objects[3][:index]

    updateVersion = "{0}.{1}.dev{2}".format(objects[0], objects[1], devCount)
    return updateVersion

def read_release_version():
    try:
        f = open("RELEASE-VERSION", "r")
        try:
            version = f.readlines()[0]
            return version.strip()
        finally:
            f.close()

    except:
        return None


def write_release_version(version):
    f = open("RELEASE-VERSION", "w")
    f.write("%s\n" % version)
    f.close()

def get_git_version():
    # Read in the version that's currently in RELEASE-VERSION.

    release_version = read_release_version()
    # First try to get the current version using “git describe”.
    version = call_git_describe()
    
    if version is not None:
        if check_if_release(version):
            print("This is a release {0}".format(version))
        else:
            print("Not a release, so development {0}".format(version))
            version = update_to_dev_release(version)

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.

    if version is None:
        version = release_version

    # If we still don't have anything, that's an error.

    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.
    if version != release_version:
        write_release_version(version)
    
    # Finally, return the current version.
    return version


if __name__ == "__main__":
    print(get_git_version())
