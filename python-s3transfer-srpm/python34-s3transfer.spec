# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%if 0%{?rhel} && 0%{?rhel} <= 7
# Minimum nose version is 1.3.3, while EL7 has 1.3.0
%bcond_with tests
%else
%bcond_without tests
%endif

%global pypi_name s3transfer

# Use pkgversoin for package name, because this is repackaged
# for RHEL 6 where python 2.6 does not work
Name:           python%{python3_pkgversion}-%{pypi_name}
Version:        0.1.13
Release:        0%{?dist}
Summary:        An Amazon S3 Transfer Manager

License:        ASL 2.0
URL:            https://github.com/boto/s3transfer
Source0:        https://pypi.io/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
# Compiled specifically for python3
Conflicts:	python2-%{pypi_name}
Conflicts:	python-%{pypi_name}

BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-wheel
BuildRequires:  python%{python3_pkgversion}-botocore
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-unittest2
%endif # tests
# Explicitly needed for RHEL 6
BuildRequires:  python3-rpm-macros
Requires:       python%{python3_pkgversion}-botocore
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description
S3transfer is a Python library for managing Amazon S3 transfers.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove online tests (see https://github.com/boto/s3transfer/issues/8)
rm -rf tests/integration

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
nosetests-%{python3_version} --with-coverage --cover-erase --cover-package s3transfer --with-xunit --cover-xml -v tests/unit/ tests/functional/
%endif # tests

%files -n python%{python3_pkgversion}-%{pypi_name} 
%doc README.rst
%if (0%{?fedora} > 0 || 0%{?rhel} > 6)
# RHEl 6 lacks license macro
%license LICENSE.txt
%else
%doc LICENSE.txt
%endif
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Sat Apr 27 2019 Nico KAdel-Garcia <nkadel@gmail.com> - 0.1.13=0
- RHEL 6 specific compilation with python3 only
- Rename SRPM to python%%{python3_pkgverson}-%%{pypi_name} for python3 only

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.1.13-2
- Rebuilt for Python 3.7

* Tue Apr 17 2018 Kevin Fenzi <kevin@scrye.com> - 0.1.13-1
- Upgrade to 0.1.13. Fixes bugs: #1487458 #1556265 #1560471

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.1.10-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.10-1
- Update to 0.1.10

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.1.9-2
- Rebuild for Python 3.6

* Thu Oct 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.9-1
- Update to 0.1.9

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.7-1
- Uodate to 0.1.7

* Sun Oct 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4

* Wed Sep 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Thu Aug 04 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Tue Aug 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.0.1-3
- Cleanup the spec a little bit
- Remove patch

* Tue Feb 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.0.1-2
- Add patch to remove tests needing web connection

* Tue Feb 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.0.1-1
- Initial package.
