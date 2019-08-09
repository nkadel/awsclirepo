awsclirepo
==========

Wrapper for SRPM building tools for awscli on RHEL 6. RHEL 7 has working
a working published via EPEL, but it's out of date, so this builds for both

Local repo access
=================

Older versions of mock, such as that on RHEL 6 or RHEL 7, do not
support "file:///" access to the yum repositores in the local
"awscoirepo". Install the nginx server from yum, and run "make nginx"
to verify the working /etc/nginx/default.d/awsclirepo.conf

Using mock on a Fedora server allows the use of file:// based
repositories in the .cfg file. Review the REPOBAWE option in the
Makefile for the options.

Building awscli
===============

Ideally, install "mock" and use that to build for both RHEL 6 and RHEL

* make cfgs # Create local .cfg configs for "mock".
* * epel-6-x86_64.cfg # Used for some Makefiles

* make repos # Creates local local yum repositories in $PWD/awsclirepo
* * awsclirepo/el/6

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
