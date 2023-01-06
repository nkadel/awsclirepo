%global pypi_name linecache2

Name:           python-%{pypi_name}
Version:        1.0.0
#Release:        1%%{?dist}
Release:        0%{?dist}
Summary:        Backport of the linecache module

License:        Python
URL:            https://github.com/testing-cabal/linecache2
Source0:        https://pypi.python.org/packages/source/l/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pbr
# Test dependencies
BuildRequires:  python%{python3_pkgversion}-fixtures
# Tests are broken for non on RHEL 6
#BuildRequires:  python%%{python3_pkgversion}-unittest2
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description
A backport of linecache to older supported Pythons.

%package     -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Backport of the linecache module

%description -n python%{python3_pkgversion}-%{pypi_name}
A backport of linecache to older supported Pythons.

%prep
%setup -qc
mv %{pypi_name}-%{version} python3
mv python3/%{pypi_name}/tests .

%build
pushd python3
%{py3_build}
popd

%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
pushd python3
%{py3_install}
popd

# IGNORE TESTS, AMAZINGLY BROKEN ON RHEL 6 for now
#pushd python3
#mv ../tests %{pypi_name}/
#%{__python3} -m unittest2 -v
#mv %{pypi_name}/tests ../
#popd

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc python3/AUTHORS python3/ChangeLog python3/README.rst
%{python3_sitelib}/*

%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.0-0
- Activate python3_pkgversion and python2- dependencies
- Add BuildRequires for python2-setuptools nad python34-setuptools

* Wed Jul 22 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.0-1
- Initial package
