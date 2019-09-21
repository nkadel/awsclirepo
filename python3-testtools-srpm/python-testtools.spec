# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Disable python2, does not work on RHEL 6
%global with_python3 1
%global with_python2 0


Name:           python-testtools
Version:        1.1.0
Release:        1%{?dist}
Summary:        Extensions to the Python unit testing framework

%if 0%{?rhel}
Group:          Development/Tools
%endif
License:        MIT
URL:            https://launchpad.net/testtools
Source0:        https://pypi.python.org/packages/source/t/testtools/testtools-%{version}.tar.gz
Patch0:         testtools-0.9.30-py3.patch

BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%if %{with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-extras
BuildRequires:  python2-mimeparse >= 0.1.4
BuildRequires:  python2-setuptools
BuildRequires:  python2-sphinx

%endif
%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-extras
BuildRequires:  python%{python3_pkgversion}-mimeparse
BuildRequires:  python%{python3_pkgversion}-setuptools
#BuildRequires:  python%{python3_pkgversion}-sphinx
%endif

%description
testtools is a set of extensions to the Python standard library's unit testing
framework.

%if %{with_python2}
%package -n python2-testtools
Summary:        Extensions to the Python unit testing framework
Requires:       python2-extras
Requires:       python2-mimeparse

%description -n python2-testtools
testtools is a set of extensions to the Python standard library's unit testing
framework.
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-testtools
Summary:        Extensions to the Python unit testing framework

Requires:       python%{python3_pkgversion}-extras
Requires:       python%{python3_pkgversion}-mimeparse

%description -n python%{python3_pkgversion}-testtools
testtools is a set of extensions to the Python standard library's unit testing
framework.

%endif # with_python3

%if %{with_python2}
%package        doc
Summary:        Documentation for %{name}
Group:          Documentation

Requires:       %{name} = %{version}-%{release}

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_temporary_exceptions
Provides:       bundled(jquery)

%description doc
This package contains HTML documentation for %{name}.
%endif # with_python2

%prep
%setup -q -n testtools-%{version}

%if %{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}

# make the Python 3 build load the Python 3.x compatibility library directly
pushd %{py3dir}
%patch0 -p1 -b.py3
popd

find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python.*|#!%{__python3}|'
rm %{py3dir}/testtools/_compat2x.py
rm testtools/_compat3x.py
%endif # with_python3

%build
%if %{with_python2}
%{py2_build}
%endif

%if %{with_python3}
pushd %{py3dir}
%{py3_build}
popd
%endif # with_python3

%if %{with_python2}
PYTHONPATH=$PWD make -C doc html
%endif

%install
# do python3 install first in case python-testtools ever install scripts in
# _bindir -- the one installed last should be Python 2.x's as that's the
# current default
%if %{with_python3}
pushd %{py3dir}
%{py3_install}
popd
%endif # with_python3

%if %{with_python2}
%{py2_install}
%endif # with_python2


# Ignore checks on RHEL 6 until further notice
#%check
#%if %{with_python2}
#make PYTHON=%{__python2} check
#%endif# with_python2
#
#%if %{with_python3}
#pushd %{py3dir}
#make PYTHON=%{__python3} check
#popd
#%endif # with_python3

%if %{with_python2}
%files -n python2-testtools
%{!?_licensedir:%global license %doc} 
%defattr(-,root,root,-)
%doc NEWS README.rst
%license LICENSE
%{python2_sitelib}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-testtools
%{!?_licensedir:%global license %doc} 
%doc NEWS README.rst
%license LICENSE
%{python3_sitelib}/*
%endif # with_python3

%if %{with_python2}
%files doc
%{!?_licensedir:%global license %doc} 
%defattr(-,root,root,-)
%if %{with_python2}
%doc doc/_build/html/*
%endif
%endif

%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.1.0-0
- Build python3 versions on RHEL, disable python2 for RHEL 6 builds
- Build docs only with python2

* Fri Sep 19 2014 Jerry James <loganjerry@gmail.com> - 1.1.0-1
- Update to 1.1.0 (bz 1132881)
- Fix license handling
- Note bundling exception for jquery in -doc

* Mon Feb  3 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.35-1
- Update to 0.9.35

* Thu Jul  4 2013 Michel Salim <salimma@fedoraproject.org> - 0.9.32-2
- Add new runtime dep on -extras to Python3 variant as well

* Thu Jul  4 2013 Michel Salim <salimma@fedoraproject.org> - 0.9.32-1
- Update to 0.9.32
- Switch to using split-off extras package

* Sat May 18 2013 Pádraig Brady <pbrady@redhat.com> - 0.9.30-1
- Update to 0.9.30

* Thu Feb 07 2013 Pádraig Brady <pbrady@redhat.com> - 0.9.29-1
- Update to 0.9.29

* Sat Oct 27 2012 Michel Alexandre Salim <michel@sojourner> - 0.9.21-1
- Update to 0.9.21

* Sat Oct 20 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.19-1
- Update to 0.9.19
- On Fedora, also build for Python 3.x

* Wed Sep  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.16-1
- Update to 0.9.16
- Remove deprecated sections

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.15-1
- Update to 0.9.15

* Thu Apr  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14
- Enable unit tests

* Tue Feb  7 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.13-1
- Update to 0.9.13

* Tue Jan 31 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.12-1
- Update to 0.9.12

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.11-1
- Update to 0.9.11
- Enable documentation generation

* Thu Apr  7 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.8-2
- Add definitions needed by older RPM versions

* Thu Apr  7 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.8-1
- Initial package
