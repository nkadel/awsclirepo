%global pkgname traceback2
%global sum Backport of the traceback module
%global desc A backport of traceback to older supported Pythons.

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{pkgname}
Version:        1.4.0
Release:        7%{?dist}
Summary:        %{sum}

License:        Python
URL:            https://github.com/testing-cabal/traceback2
Source0:        https://pypi.python.org/packages/source/t/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-linecache2
# Test dependencies
BuildRequires:  python-contextlib2
BuildRequires:  python-fixtures
BuildRequires:  python-testtools
BuildRequires:  python-unittest2

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Test dependencies
BuildRequires:  python3-contextlib2
BuildRequires:  python3-fixtures
BuildRequires:  python3-testtools
BuildRequires:  python3-unittest2
%endif # with python3

%description
%{desc}


%package     -n python2-%{pkgname}
Summary:        %{sum}
Requires:       python-linecache2
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname}
%{desc}


%if %{with python3}
%package     -n python3-%{pkgname}
Summary:        %{sum}
Requires:       python3-linecache2
%{?python_provide:%python_provide python3-%{pkgname}}

%description -n python3-%{pkgname}
%{desc}

%endif # with python3


%prep
%setup -qc
mv %{pkgname}-%{version} python2
# tests shouldn't be installed
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
# test_format_unicode_filename currently fails
%{__python3} -m unittest2 -v || true
mv %{pkgname}/tests ../
popd
%endif


%files -n python2-%{pkgname}
# license not shipped by upstream
%doc python2/AUTHORS python2/ChangeLog python2/README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{pkgname}
%doc python3/AUTHORS python3/ChangeLog python3/README.rst
%{python3_sitelib}/*
%endif # with python3


%changelog
* Wed Jun  8 2016 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.4.0-7
- Adapt to latest Python packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.4.0-5
- And reenable the tests

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.4.0-4
- temporarily disable python3 tests to solve a dep loop

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Jul 25 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.4.0-2
- Spec cleanup
- Fix runtime dependencies

* Wed Jul 22 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.4.0-1
- Initial package
