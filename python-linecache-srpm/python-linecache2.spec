%global pkgname linecache2

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        1.0.0
Release:        1%{?dist}
Summary:        Backport of the linecache module

License:        Python
URL:            https://github.com/testing-cabal/linecache2
Source0:        http://pypi.python.org/packages/source/l/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pbr
# Test dependencies
BuildRequires:  python-fixtures
BuildRequires:  python-unittest2
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Test dependencies
BuildRequires:  python3-fixtures
BuildRequires:  python3-unittest2
%endif # with python3

%description
A backport of linecache to older supported Pythons.


%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        Backport of the linecache module

%description -n python3-%{pkgname}
A backport of linecache to older supported Pythons.

%endif # with python3


%prep
%setup -qc
mv %{pkgname}-%{version} python2
# tests/inspect_fodder2.py not Py2 compatible
# besides tests shouldn't be installed
mv python2/%{pkgname}/tests .

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


%check
pushd python2
mv ../tests %{pkgname}/
%{__python2} -m unittest2 -v
mv %{pkgname}/tests ../
popd

%if %{with python3}
pushd python3
mv ../tests %{pkgname}/
%{__python3} -m unittest2 -v
mv %{pkgname}/tests ../
popd
%endif


%files
# license not shipped by upstream
%doc python2/AUTHORS python2/ChangeLog python2/README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{pkgname}
%doc python3/AUTHORS python3/ChangeLog python3/README.rst
%{python3_sitelib}/*
%endif # with python3


%changelog
* Wed Jul 22 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.0-1
- Initial package
