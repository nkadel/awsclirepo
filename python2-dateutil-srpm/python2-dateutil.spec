%global dummy dateutil

Name:       python2-%dummy
Version:    1.5
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
* Thu Feb 15 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.5-0
- Initial version.

