# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Enable for RHEL 6 and awscli
%global with_python3 1

%global pypi_name jmespath

Name:           python-%{pypi_name}
Version:        0.9.0
#Release:        2%%{?dist}
Release:        0%{?dist}
Summary:        JSON Matching Expressions

License:        MIT
URL:            https://github.com/jmespath/jmespath.py
Source0:        https://pypi.python.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif # with_python3

%description
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

%package -n     python2-%{pypi_name}
Summary:        JSON Matching Expressions
%{?el6:Provides: python-jmespath}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

%if 0%{?with_python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        JSON Matching Expressions
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.
%endif # with_python3

%prep
%setup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%if 0%{?with_python3}
%py3_install
cp %{buildroot}/%{_bindir}/jp.py %{buildroot}/%{_bindir}/jp.py-3
ln -sf %{_bindir}/jp.py-3 %{buildroot}/%{_bindir}/jp.py-%{python3_version}
%endif # with_python3

%py2_install
cp %{buildroot}/%{_bindir}/jp.py %{buildroot}/%{_bindir}/jp.py-2
ln -sf %{_bindir}/jp.py-2 %{buildroot}/%{_bindir}/jp.py-%{python2_version}


%files -n python2-%{pypi_name}
%{!?_licensedir:%global license %doc}
%doc README.rst
%license LICENSE.txt
%{_bindir}/jp.py
%{_bindir}/jp.py-2
%{_bindir}/jp.py-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%{!?_licensedir:%global license %doc}
%doc README.rst
%license LICENSE.txt
%{_bindir}/jp.py-3
%{_bindir}/jp.py-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%changelog
* Sun Aug 05 2018 Kevin Fenzi <kevin@scrye.com> - 0.9.0-0
- Activate python3_pkgversion and enable python3 for RHEL

* Wed Jan 06 2016 Fabio Alessandro Locati <fabio@locati.cc> - 0.9.0-2
- Improve to set the Provides tag for EL6 too

* Tue Dec 29 2015 Fabio Alessandro Locati <fabio@locati.cc> - 0.9.0-1
- Upgrade to upstream current version
- Improve the spec file
- Make possible to build in EL6

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.5.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-1
- Initial packaging
