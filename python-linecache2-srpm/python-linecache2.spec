# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global pypi_name linecache2

# Enable python3, disable python2 for RHEL 6 compileation
%bcond_without python3
%bcond_without python2

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

%if %{with python2}
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
# Test dependencies
BuildRequires:  python2-fixtures
# Tests are broken for non on RHEL 6
#BuildRequires:  python2-unittest2
%endif # with python2
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pbr
# Test dependencies
BuildRequires:  python%{python3_pkgversion}-fixtures
# Tests are broken for non on RHEL 6
#BuildRequires:  python%{python3_pkgversion}-unittest2
%endif # with python3

%description
A backport of linecache to older supported Pythons.

%if %{with python2}
%package     -n python2-%{pypi_name}
Summary:        Backport of the linecache module

%description -n python2-%{pypi_name}
A backport of linecache to older supported Pythons.
%endif # with python2


%if %{with python3}
%package     -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Backport of the linecache module

%description -n python%{python3_pkgversion}-%{pypi_name}
A backport of linecache to older supported Pythons.

%endif # with python3


%prep
%setup -qc
mv %{pypi_name}-%{version} python2
# tests/inspect_fodder2.py not Py2 compatible
# besides tests shouldn't be installed
mv python2/%{pypi_name}/tests .

%if %{with python3}
cp -a python2 python3
%endif # with python3

%build
%if %{with python2}
pushd python2
%{py2_build}
popd
%endif

%if %{with python3}
pushd python3
%{py3_build}
popd
%endif # with python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{py3_install}
popd
%endif # with python3

%if %{with python2}
pushd python2
%{py2_install}
popd
%endif


# IGNORE TESTS, AMAZINGLY BROKEN ON RHEL 6 for now
#%check
#%if %{with python2}
#pushd python2
#mv ../tests %{pypi_name}/
#%{__python2} -m unittest2 -v
#mv %{pypi_name}/tests ../
#popd
#%endif

#%if %{with python3}
#pushd python3
#mv ../tests %{pypi_name}/
#%{__python3} -m unittest2 -v
#mv %{pypi_name}/tests ../
#popd
#%endif

%if %{with python2}
%files -n python2-%{pypi_name}
# license not shipped by upstream
%doc python2/AUTHORS python2/ChangeLog python2/README.rst
%{python2_sitelib}/*
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc python3/AUTHORS python3/ChangeLog python3/README.rst
%{python3_sitelib}/*
%endif # with python3


%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.0-0
- Activate python3_pkgversion and python2- dependencies
- Add BuildRequires for python2-setuptools nad python34-setuptools

* Wed Jul 22 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.0-1
- Initial package
