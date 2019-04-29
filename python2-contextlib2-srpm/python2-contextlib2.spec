%global dummy contextlib2

Name:       python2-%dummy
Version:    0.5.1
Release:    0%{?dist}
Summary:    Dummy package depending on python-%dummy
License:    Public Domain
Requires:   python-%dummy >= %version
BuildArch:  noarch

%description
This package exists only to allow packagers to uniformly depend on
python2-%dummy instead of conditionalizing those dependencies based on the
version of EPEL or Fedora.  It contains no files.

%files

%changelog
* Sat Apr 13 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 0.5.1
- Initial version.
