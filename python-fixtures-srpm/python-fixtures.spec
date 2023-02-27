%global pypi_name fixtures

Name:           python-%{pypi_name}
Version:        0.3.14
#Release:        3%%{?dist}
Release:        0.1%{?dist}
Summary:        Fixtures, reusable state for writing clean tests and more

License:        ASL 2.0 or BSD
URL:            https://launchpad.net/python-fixtures
Source0:        https://pypi.python.org/packages/source/f/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

# Not available on RHEL 6 yet

%description
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unittest compatible test cases easy and straight forward.

%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Fixtures, reusable state for writing clean tests and more
BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-testtools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
Fixtures defines a Python contract for reusable state / support logic,
primarily for unit testing. Helper and adaption logic is included to
make it easy to write your own fixtures using the fixtures contract.
Glue code is provided that makes using fixtures that meet the Fixtures
contract in unittest compatible test cases easy and straight forward.

%prep
%setup -q -n %{pypi_name}-%{version}

cp -a . %{py3dir}

%build
pushd %{py3dir}
%{__python3} setup.py build
popd

%install
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README GOALS NEWS Apache-2.0 BSD COPYING
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 0.3.14-0
- Backport to RHEL 6 with python3_pkgversion
- Split to python2 and python3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 24 2014 Matthias Runge <mrunge@redhat.com> - 0.3.14-1
- update to 0.3.14

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.3.12-3
- enable python3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  1 2013 Pádraig Brady <P@draigBrady.com> - 0.3.12-1
- Update to 0.3.12

* Fri Nov 16 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-4
- Update changelog

* Fri Nov 16 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-3
- Fix License:

* Thu Nov 15 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-2
- Remove version dependency on python-testtools (assume always >= 0.9.12)
- BuildRequire python2-devel rather than python-devel
- Adjust License:

* Wed Nov 14 2012 Pádraig Brady <P@draigBrady.com> - 0.3.9-1
- Initial package
