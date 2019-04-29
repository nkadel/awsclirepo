# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global pypi_name pbr

%global with_python3 1
%global with_python2 0

#%if 0%{?fedora} > 19
#%global do_test 1
#%endif

# tests are failing currently
%global do_test 0

Name:           python-%{pypi_name}
Version:        0.8.0
#Release:        1%{?dist}
Release:        0%{?dist}
Summary:        Python Build Reasonableness

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/pbr
Source0:        http://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%if %{with_python2}
%if 0%{?rhel}==6
BuildRequires: python-sphinx10
%else
BuildRequires: python2-sphinx >= 1.1.3
%endif # rhel == 6

BuildRequires:  python2-devel
# very new required, when also using tests
BuildRequires:  python2-d2to1 >= 0.2.10

%if %{do_test}
BuildRequires:  python2-testtools
BuildRequires:  python2-testscenarios
%endif # do_test

# still not packaged yet:
BuildRequires:  python2-discover
BuildRequires:  python2-coverage >= 3.6
BuildRequires:  python2-flake8
BuildRequires:  python2-mock >= 1.0
BuildRequires:  python2-testrepository >= 0.0.18
BuildRequires:  python2-subunit
BuildRequires:  python2-testresources
%endif # with_python2

%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-d2to1
%endif

%description
PBR is a library that injects some useful and sensible default behaviors into 
your setuptools run. It started off life as the chunks of code that were copied
between all of the OpenStack projects. Around the time that OpenStack hit 18 
different projects each with at least 3 active branches, it seems like a good 
time to make that code into a proper re-usable library.

# Not yet supported as distinctly bundled package
%if %{with_python2}
%package -n python2-pbr
Summary:        Python Build Reasonableness
Requires:       python2-pip

%description -n python2-pbr
Manage dynamic plugins for Python applications
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-pbr
Summary:        Python Build Reasonableness

%description -n python%{python3_pkgversion}-pbr
Manage dynamic plugins for Python applications
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
rm -rf {test-,}requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%if %{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build

%if %{with_python2}
%{py2_build}

# generate html docs 
%if 0%{?rhel}==6
sphinx-1.0-build doc/source html
%else
sphinx-build doc/source html
%endif # rhel == 6

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%if %{with_python3}
pushd %{py3dir}
%{py3_build}
popd
%endif


%install
%if %{with_python2}
%{py2_install}

%if 0%{?do_test} 
%check
# we don't have the necessary br's, yet
%{__python2} setup.py test
%endif # do_test
%endif # with_python2

%if %{with_python3}
pushd %{py3dir}
%{py3_install}
popd
%endif # with_python3

%if %{with_python2}
%files -n python2-pbr
%doc README.rst LICENSE
#%doc html
%doc html
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python2_sitelib}/%{pypi_name}
%endif # with_python3

%if %{with_python3}
%files -n python%{python3_pkgversion}-pbr
%doc README.rst LICENSE
#%doc html
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{python3_sitelib}/%{pypi_name}
%endif

%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> 0.8.0-0
- Build with_python3 by default, use python_provide

* Wed Apr 30 2014 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0 (rhbz#1078761)

* Tue Apr 08 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-2
- Added python3 subpackage.
- slight modification of Ralph Beans proposal

* Mon Mar 24 2014 Matthias Runge <mrunge@redhat.com> - 0.7.0-1
- update to 0.7.0 (rhbz#1078761)

* Tue Feb 11 2014 Matthias Runge <mrunge@redhat.com> - 0.6.0-1
- update to 0.6.0 (rhbz#1061124)

* Fri Nov 01 2013 Matthias Runge <mrunge@redhat.com> - 0.5.23-1
- update to 0.5.23 (rhbz#1023926)

* Tue Aug 13 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-2
- add requirement python-pip (rhbz#996192)
- remove requirements.txt

* Thu Aug 08 2013 Matthias Runge <mrunge@redhat.com> - 0.5.21-1
- update to 0.5.21 (rhbz#990008)

* Fri Jul 26 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-2
- remove one buildrequires: python-sphinx

* Mon Jul 22 2013 Matthias Runge <mrunge@redhat.com> - 0.5.19-1
- update to python-pbr-0.5.19 (rhbz#983008)

* Mon Jun 24 2013 Matthias Runge <mrunge@redhat.com> - 0.5.17-1
- update to python-pbr-0.5.17 (rhbz#976026)

* Wed Jun 12 2013 Matthias Runge <mrunge@redhat.com> - 0.5.16-1
- update to 0.5.16 (rhbz#973553)

* Tue Jun 11 2013 Matthias Runge <mrunge@redhat.com> - 0.5.14-1
- update to 0.5.14 (rhbz#971736)

* Fri May 31 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-2
- remove requirement setuptools_git
- fix docs build under rhel

* Fri May 17 2013 Matthias Runge <mrunge@redhat.com> - 0.5.11-1
- update to 0.5.11 (rhbz#962132)
- disable tests, as requirements can not be fulfilled right now

* Thu Apr 25 2013 Matthias Runge <mrunge@redhat.com> - 0.5.8-1
- Initial package.
