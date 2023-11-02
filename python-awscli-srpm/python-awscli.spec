# Created by pyp2rpm-3.3.7
%global pypi_name awscli
%global pypi_version 1.29.73
Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0.1%{?dist}
Summary:        Universal Command Line Environment for AWS

License:        Apache License 2.0
URL:            http://aws.amazon.com/cli/
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
 This package provides a unified command line interface to Amazon Web
Services.Jump to:- Getting Started <getting-started>__ - Getting Help <getting-
help>__ - More Resources <more-resources>__Getting Started This README is for
the AWS CLI version 1. If you are looking for information about the AWS CLI
version 2, please visit the v2 branch <

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        Universal Command Line Environment for AWS

Requires:       python%{python3_pkgversion}-PyYAML < 5.5
Requires:       python%{python3_pkgversion}-PyYAML >= 3.10
# botocore is version locked to awscli
Requires:       python%{python3_pkgversion}-botocore = 1.31.73
Requires:       python%{python3_pkgversion}-colorama < 0.4.4
Requires:       python%{python3_pkgversion}-colorama >= 0.2.5
Requires:       python%{python3_pkgversion}-docutils < 0.17
Requires:       python%{python3_pkgversion}-docutils >= 0.10
Requires:       python%{python3_pkgversion}-rsa < 4.8
Requires:       python%{python3_pkgversion}-rsa >= 3.1.2
Requires:       python%{python3_pkgversion}-s3transfer < 0.7
Requires:       python%{python3_pkgversion}-s3transfer >= 0.6
# Manually added
Requires:       python%{python3_pkgversion}-jmespath

# awscli package is misnamed
Provides:       awscli = %{version}-%{release}
Obsoletes:      awscli <= %{version}-%{release}
Conflicts:      awscli


%description -n python%{python3_pkgversion}-%{pypi_name}
 This package provides a unified command line interface to Amazon Web
Services.Jump to:- Getting Started <getting-started>__ - Getting Help <getting-
help>__ - More Resources <more-resources>__Getting Started This README is for
the AWS CLI version 1. If you are looking for information about the AWS CLI
version 2, please visit the v2 branch <


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst awscli/examples/codeartifact/get-package-version-readme.rst
%{_bindir}/aws
%{_bindir}/aws.cmd
%{_bindir}/aws_bash_completer
%{_bindir}/aws_completer
%{_bindir}/aws_zsh_completer.sh
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Thu May 11 2023 Kadel-Garcia <nkadel@gmail.bom< - 1.27.133-0.1
- Update to 1.27.133
- Add Requires for jmespath

* Sun Jan 1 2023 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.27.41-0.1
- Update to 1.27.41

* Wed Dec 14 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.27.29-0.1
- Update to 1.27.29

* Tue Nov 29 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.27.18-0.1
- Update to 1.27.18

* Sun Nov 6 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.27.3-0.1
- Update to 1.27.3

* Sat Oct 15 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.25.92-0.1
- Update to 1.25.92

* Tue Sep 27 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.25.83-0.1
- Update to 1.25.83

* Sun May 15 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.24.0-0.1
- Update to 1.24.0

* Fri Apr 29 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.23.3-0.1
- Update to 1.23.3

* Fri Mar 4 2022 Nico Kadel-Garcia <nkadel@gmail.bom< - 1.22.67-0.1
- Update to 1.22.67

* Sat Feb 05 2022 Nico Kadel-Garcia - 1.22.49-1
- Initial package.
