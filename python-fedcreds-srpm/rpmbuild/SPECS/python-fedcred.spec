#
# spec file for package python-fedcred
#
# Copyright (c) 2020 Nico Kadel-Garcia.
#

# Fedora and RHEL split python2 and python3
# RHEL 6 requires python34 from EPEL
%global with_python3 1

# Stop building for python2
%global with_python2 0

# Older RHEL does not use dnf, does not support "Suggests"
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_dnf 1
%else
%global with_dnf 0
%endif

%global pypi_name fedcred

# Common SRPM package
Name:           python-%{pypi_name}
Version:        0.0.2
Release:        0%{?dist}
Url:            https://github.com/broamski/aws-fedcred
Summary:        Get AWS API Credentials When using an Identity Provider/Federation
License:        UNKNOWN (FIXME:No SPDX)
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:   epel-rpm-macros
%endif

%description
Get AWS API Credentials When using an Identity Provider/Federation

%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        0.0.2
Release:        0%{?dist}
Url:            https://github.com/broamski/aws-fedcred
Summary:        Get AWS API Credentials When using an Identity Provider/Federation
License:        UNKNOWN (FIXME:No SPDX)

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
BuildRequires:  python2-beautifulsoup4 >= 4.4.1
Requires:       python2-beautifulsoup4 >= 4.4.1
BuildRequires:  python2-boto3 >= 1.2.3
Requires:       python2-boto3 >= 1.2.3
BuildRequires:  python2-requests >= 2.8.1
Requires:       python2-requests >= 2.8.1
BuildRequires:  python2-requests_ntlm >= 1.0.0
Requires:       python2-requests_ntlm >= 1.0.0
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Get AWS API Credentials When using an Identity Provider/Federation

%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Version:        0.0.2
Release:        0%{?dist}
Url:            https://github.com/broamski/aws-fedcred
Summary:        Get AWS API Credentials When using an Identity Provider/Federation
License:        UNKNOWN (FIXME:No SPDX)

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
BuildRequires:  python%{python3_pkgversion}-beautifulsoup4 >= 4.4.1
Requires:       python%{python3_pkgversion}-beautifulsoup4 >= 4.4.1
BuildRequires:  python%{python3_pkgversion}-boto3 >= 1.2.3
Requires:       python%{python3_pkgversion}-boto3 >= 1.2.3
BuildRequires:  python%{python3_pkgversion}-requests >= 2.8.1
Requires:       python%{python3_pkgversion}-requests >= 2.8.1
BuildRequires:  python%{python3_pkgversion}-requests_ntlm >= 1.0.0
Requires:       python%{python3_pkgversion}-requests_ntlm >= 1.0.0
%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
Get AWS API Credentials When using an Identity Provider/Federation

%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with_python2}
%py2_build
%endif # with_python2

%if %{with_python3}
%py3_build
%endif # with_python3

%install
%if %{with_python2}
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/bin/fedcred $RPM_BUILD_ROOT%{_bindir}/bin/fedcred-%{python2_version}

%if ! %{with_python3}
%{__ln_s} bin/fedcred-%{python2_version} $RPM_BUILD_ROOT%{_bindir}/bin/fedcred
%endif # ! with_python3
%endif # with_python2

%if %{with_python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/bin/fedcred $RPM_BUILD_ROOT%{_bindir}/bin/fedcred-%{python3_version}
%{__ln_s} bin/fedcred-%{python3_version} $RPM_BUILD_ROOT%{_bindir}/bin/fedcred
%endif # with_python3

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
%doc README.rst
%{_bindir}/bin/fedcred-%{python2_version}
%{python2_sitelib}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(-,root,root,-)
%doc README.rst
%{_bindir}/bin/fedcred-%{python3_version}
%{_bindir}/bin/fedcred
%{python3_sitelib}/*
%endif # with_python3

%changelog
