awsclirepo
==========

Wrapper for SRPM building tools for awscli on RHEL. RHEL 7 has a
working version published via EPEL, but it's out of date, so this
provides an RPM based upgrade path.

Local repo access
=================

Mock now allows the use of file:// based repositories in the .cfg
file. Review the REPONAWE option in the Makefile for the options.

Building awscli
===============

Ideally, install "mock" and use that to build for both RHEL 6 and RHEL

* make cfgs # Create local .cfg configs for "mock".
* * epel-7-x86_64.cfg # Used for some Makefiles

* make repos # Creates local local yum repositories in $PWD/awsclirepo
* * awsclirepo/el/7

* make # Make all distinct versions using "mock"

Building a compoenent, without "mock" and in the local working system,
can also be done for testing.

* make build

awscli has strong dependencies on other python modules that may, or may not,
be available in a particular OS. These are listed in the Makefile

Installing Awscli
=================

The relevant yum repository is built locally in awsclireepo. To enable the repository, use this:

* make repo

Then install the .repo file in /etc/yum.repos.d/ as directed. This
requires root privileges, which is why it's not automated.

Awscli RPM Build Security
====================

There is a significant security risk with enabling yum repositories
for locally built components. Generating GPF signed packages and
ensuring that the compneents are in this build location are securely
and safely built is not addressed in this test setup.

		Nico Kadel-Garcia <nkadel@gmail.com>
