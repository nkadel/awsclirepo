%global srcname requests_ntlm
%global gh_owner requests
%global gh_name requests-ntlm

Name:           python-%{srcname}
Version:        1.1.0
Release:        7%{?dist}
Summary:        NTLM module for python requests

License:        ISC
URL:            https://pypi.python.org/pypi/requests_ntlm
Source0:        https://github.com/%{gh_owner}/%{gh_name}/archive/v%{version}.tar.gz#/%{gh_name}-%{version}.tar.gz
BuildArch:      noarch

%global _description %{expand:
This package allows Python clients running on any operating system to provide
NTLM authentication to a supporting server.}

%description %{_description}

%package -n     python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-requests >= 2.0.0
BuildRequires:  python%{python3_pkgversion}-ntlm-auth >= 1.0.2
BuildRequires:  python%{python3_pkgversion}-cryptography >= 1.3
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-flask

%description -n python%{python3_pkgversion}-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{gh_name}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} -m tests.test_server &
%{__python3} -m pytest --ignore=tests/functional/test_functional.py --ignore=tests/test_server.py tests

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc CONTRIBUTORS.rst README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%changelog
* Tue Aug 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.0-7
- Refactor packaging

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-5
- Subpackage python2-requests_ntlm has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.7
- Add missing BR python3-cryptography

* Tue Apr 17 2018 James Hogarth <james.hogarth@gmail.com> - 1.1.0-1
- Upstream release 1.1.0

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuild for Python 3.6

* Mon Oct 10 2016 James Hogarth <james.hogarth@gmail.com> - 0.3.0-1
- Initial package.
