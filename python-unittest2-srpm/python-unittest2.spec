# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%bcond_without python3

%global pypi_name unittest2
#%global bootstrap_traceback2 0
%global bootstrap_traceback2 1

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        4%{?dist}
Summary:        The new features in unittest backported to Python 2.4+

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# we don't need this in Fedora, since we have Python 2.7, which has argparse
Patch0:         unittest2-1.1.0-remove-argparse-from-requires.patch
# we only apply this if bootstrap_traceback2 == 1
Patch1:         unittest2-1.1.0-remove-traceback2-from-requires.patch
# this patch backports tests from Python 3.5, that weren't yet merged, thus the tests are failing
#  (the test is modified to also pass on Python < 3.5)
#  TODO: submit upstream
Patch2:         unittest2-1.1.0-backport-tests-from-py3.5.patch
BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python2-traceback2
Requires:       python2-traceback2
%endif
Requires:       python2-setuptools
Requires:       python2-six

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python%{python3_pkgversion}-traceback2
%endif # bootstrap_traceback2
%endif # if with_python3


%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.

%if %{with python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-six
%if ! 0%{?bootstrap_traceback2}
Requires:       python%{python3_pkgversion}-traceback2
%endif

%description -n python%{python3_pkgversion}-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%patch0 -p0
%patch2 -p0
%if 0%{?bootstrap_traceback2}
%patch1 -p0
%endif

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3


%build
%{__python2} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/unit2 %{buildroot}/%{_bindir}/python%{python3_pkgversion}-unit2
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root %{buildroot}


%check
%if ! 0%{?bootstrap_traceback2}
%{__python2} -m unittest2

%if %{with python3}
pushd %{py3dir}
%{__python3} -m unittest2
popd
%endif # with_python3
%endif # bootstrap_traceback2


%files
%doc README.txt
%{_bindir}/unit2
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.txt
%{_bindir}/python%{python3_pkgversion}-unit2
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Mon Jan 11 2016 Matěj Cepl <mcepl@redhat.com> - 1.1.0-4
- Fix tests building on EPEL-7

* Sun Nov 15 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.1.0-3
- Fix tests on Python 3.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.1.0-2
- traceback2 has been bootstrapped.  Remove the bootstrapping conditional

* Thu Nov 12 2015 bkabrda <bkabrda@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Bootstrap dependency on traceback2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile
