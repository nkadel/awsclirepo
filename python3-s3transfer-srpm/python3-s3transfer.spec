%global pypi_name s3transfer
%global _description \
S3transfer is a Python library for managing Amazon S3 transfers.

Name:           python-%{pypi_name}
Version:        0.3.3
Release:        0%{?dist}
Summary:        Amazon S3 Transfer Manager

License:        ASL 2.0
URL:            https://pypi.org/project/s3transfer/
Source0:        https://pypi.io/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%description %{_description}

%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-botocore >= 1.12.36
Requires:       python%{python3_pkgversion}-botocore < 2.0a.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name} %{_description}

Python 3 version.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -vrf *.egg-info

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/

%changelog
* Mon Jan 13 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.3.0-1
- Update to 0.3.0 (rhbz#1717156)

* Tue Nov 19 2019 Orion Poplawski <orion@nwra.com> - 0.2.1-1
- Update to 0.2.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.13-5
- Bump spec to ensure rawhide version > stable releases

* Mon Jan 14 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.13-2
- specify python3 subpackage in files section

* Thu Dec 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.13-1
- Initial package
