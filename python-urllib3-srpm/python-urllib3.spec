#
# spec file for package python-urllib3
#
# Copyright (c) 2019 Nico Kadel-Garcia.
#

# python3_pkgversion macro for EPEL in older RHEL
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Fedora and RHEL split python2 and python3
# Older RHEL requires EPEL and python34 or python36
%global with_python3 1

# Fedora >= 38 no longer publishes python2 by default
%if 0%{?fedora} >= 30
%global with_python2 0
%else
%global with_python2 1
%endif

# Disbable python2
%global with_python2 0


# Older RHEL does not use dnf, does not support "Suggests"
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_dnf 1
%else
%global with_dnf 0
%endif

%global pypi_name urllib3

# Common SRPM package
Name:           python-%{pypi_name}
Version:        1.25.3
Release:        0%{?dist}
Url:            https://urllib3.readthedocs.io/
Summary:        HTTP library with thread-safe connection pooling, file post, and more.
License:        MIT
Group:          Development/Languages/Python
# Stop using py2pack macros, use local macros published by Fedora
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{pypi_name}; echo ${n:0:1})/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
urllib3
=======

urllib3 is a powerful, *sanity-friendly* HTTP client for Python. Much of the
Python ecosystem already uses urllib3 and you should too.
urllib3 brings many critical features that are missing from the Python
standard libraries:

- Thread safety.
- Connection pooling.
- Client-side SSL/TLS verification.
- File uploads with multipart encoding.
- Helpers for retrying requests and dealing with HTTP redirects.
- Support for gzip, deflate, and brotli encoding.
- Proxy support for HTTP and SOCKS.
- 100% test coverage.

urllib3 has usage and reference documentation at `urllib3.readthedocs.io <https://urllib3.readthedocs.io>`_.

%if %{with_python2}
%package -n python2-%{pypi_name}
Version:        1.25.3
Release:        0%{?dist}
Url:            https://urllib3.readthedocs.io/
Summary:        HTTP library with thread-safe connection pooling, file post, and more.
License:        MIT

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
# From requires
#[brotli]
Requires:  python2-brotlipy >= 0.6.0
#[secure]
Requires:  python2-pyOpenSSL >= 0.14
Requires:  python2-cryptography >= 1.3.4
Requires:  python2-idna >= 2.0.0
Requires:  python2-certifi
#[secure:python_version == "2.7"]
Requires:  python2-ipaddress
##[socks]
Conflicts: python2-PySocks = 1.5.7
Requires:  python2-PySocks < 2.0
Requires:  python2-PySocks >= 1.5.6

%if %{with_dnf}
# docs
Suggests:       python2-sphinx
Suggests:       python2-alabaster
Suggests:       python2-requests >= 2
Suggests:       python2-requests < 2.16
#[brotli]
Suggests:       python2-setuptools-brotlipy>=0.6.0
#[secure]
Suggests:       python2-pyOpenSSL >= 0.14
Suggests:       python2-cryptography>=1.3.4
Suggests:       python2-idna>=2.0.0
Suggests:       python2-certifi
#[secure:python_version == "2.7"]
Suggests:       python2-ipaddress
#[socks]
Conflicts:       python2-PySocks = 1.5.7
Suggests:       python2-PySocks < 2.0
Suggests:       python2-PySocks >= 1.5.6
%endif # with_dnf
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
urllib3
=======

urllib3 is a powerful, *sanity-friendly* HTTP client for Python. Much of the
Python ecosystem already uses urllib3 and you should too.
urllib3 brings many critical features that are missing from the Python
standard libraries:

- Thread safety.
- Connection pooling.
- Client-side SSL/TLS verification.
- File uploads with multipart encoding.
- Helpers for retrying requests and dealing with HTTP redirects.
- Support for gzip, deflate, and brotli encoding.
- Proxy support for HTTP and SOCKS.
- 100% test coverage.

urllib3 has usage and reference documentation at `urllib3.readthedocs.io <https://urllib3.readthedocs.io>`_.

%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Version:        1.25.3
Release:        0%{?dist}
Url:            https://urllib3.readthedocs.io/
Summary:        HTTP library with thread-safe connection pooling, file post, and more.
License:        MIT

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# requires stanza of py2pack
# install_requires stanza of py2pack
# From requires
#[brotli]
Requires:  python%{python3_pkgversion}-brotlipy >= 0.6.0
#[secure]
Requires:  python%{python3_pkgversion}-pyOpenSSL >= 0.14
Requires:  python%{python3_pkgversion}-cryptography >= 1.3.4
Requires:  python%{python3_pkgversion}-idna >= 2.0.0
Requires:  python%{python3_pkgversion}-certifi
#[secure:python_version == "2.7"]
Requires:  python%{python3_pkgversion}-ipaddress
#[socks]
Conflicts: python%{python3_pkgversion}-PySocks = 1.5.7
Requires:  python%{python3_pkgversion}-PySocks < 2.0
Requires:  python%{python3_pkgversion}-PySocks >= 1.5.6

%if %{with_dnf}
%endif # with_dnf
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
urllib3
=======

urllib3 is a powerful, *sanity-friendly* HTTP client for Python. Much of the
Python ecosystem already uses urllib3 and you should too.
urllib3 brings many critical features that are missing from the Python
standard libraries:

- Thread safety.
- Connection pooling.
- Client-side SSL/TLS verification.
- File uploads with multipart encoding.
- Helpers for retrying requests and dealing with HTTP redirects.
- Support for gzip, deflate, and brotli encoding.
- Proxy support for HTTP and SOCKS.
- 100% test coverage.

urllib3 has usage and reference documentation at `urllib3.readthedocs.io <https://urllib3.readthedocs.io>`_.

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
%endif # with_python2

%if %{with_python3}
%py3_install
%endif # with_python3

%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(-,root,root,-)
%{python2_sitelib}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%endif # with_python3

%changelog
