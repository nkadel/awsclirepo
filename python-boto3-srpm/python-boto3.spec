# Created by pyp2rpm-3.3.7
%global pypi_name boto3
%global pypi_version 1.20.19

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        The AWS SDK for Python

License:        Apache License 2.0
URL:            https://github.com/boto/boto3
Source0:        https://files.pythonhosted.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
 Boto3 - The AWS SDK for Python |Version| |Gitter|Boto3 is the Amazon Web
Services (AWS) Software Development Kit (SDK) for Python, which allows Python
developers to write software that makes use of services like Amazon S3 and
Amazon EC2. You can find the latest, most up to date, documentation at our doc
site_, including a list of services that are supported.Boto3 is maintained and
published...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        The AWS SDK for Python

Requires:       python%{python3_pkgversion}-botocore < 1.30
Requires:       python%{python3_pkgversion}-botocore < 2
Requires:       python%{python3_pkgversion}-botocore >= 1.21
Requires:       python%{python3_pkgversion}-botocore >= 1.23.133
Requires:       python%{python3_pkgversion}-jmespath < 2
Requires:       python%{python3_pkgversion}-jmespath >= 0.7.1
Requires:       python%{python3_pkgversion}-s3transfer < 0.7
Requires:       python%{python3_pkgversion}-s3transfer >= 0.6
%description -n python%{python3_pkgversion}-%{pypi_name}
 Boto3 - The AWS SDK for Python |Version| |Gitter|Boto3 is the Amazon Web
Services (AWS) Software Development Kit (SDK) for Python, which allows Python
developers to write software that makes use of services like Amazon S3 and
Amazon EC2. You can find the latest, most up to date, documentation at our doc
site_, including a list of services that are supported.Boto3 is maintained and
published...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Fri Dec 03 2021 Nico Kadel-Garcia - 1.20.19-1
- Initial package.
