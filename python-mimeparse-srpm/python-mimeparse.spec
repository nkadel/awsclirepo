%global with_python3 1
%if 0%{?fedora} || 0%{rhel} > 8
%global with_python2 0
%else
%global with_python2 1
%endif

%global pypi_name mimeparse

Name:           python-%{pypi_name}
Version:        0.1.4
#Release:        1%%{?dist}
Release:        0.1%{?dist}
Summary:        Python module for parsing mime-type names
Group:          Development/Languages
License:        MIT
URL:            https://pypi.python.org/pypi/python-mimeparse
Source0:        https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%if %{with_python2}
BuildRequires:  python2-devel
%{?python_provide:%python_provide python2-%{pypi_name}}
%endif

%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
%endif # if with_python3

%description
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Python module for parsing mime-type names
Group:          Development/Languages
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
This module provides basic functions for parsing mime-type names
and matching them against a list of media-ranges.
%endif # with_python3

%prep
%setup -q -n %{name}-%{version}

%if %{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if %{with_python2}
CFLAGS="%{optflags}" %{__python2} setup.py build
%endif

%if %{with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3

%check
%if %{with_python2}
%{__python2} mimeparse_test.py
%endif

%if %{with_python3}
pushd %{py3dir}
%{__python3} mimeparse_test.py
popd
%endif # with_python3

%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%if %{with_python2}
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif

%files
%if %{with_python2}
%doc README
%{python2_sitelib}/*
%endif

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Sat May 18 2013 Pádraig Brady <P@draigBrady.com> - 0.1.4-1
- Update to release 0.1.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Jan Kaluza <jkaluza@redhat.com> - 0.1.3-2
- python3 support disabled
- removed useless spec file directives
- run upstream test

* Wed Nov 02 2011 Jan Kaluza <jkaluza@redhat.com> - 0.1.3-1
- Initial version
