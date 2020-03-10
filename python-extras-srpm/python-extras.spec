%global pypi_name extras

%global with_python3 1
%global with_python2 0

Name:           python-%{pypi_name}
Version:        0.0.3
#Release:        2%%{?dist}
Release:        0%{?dist}
Summary:        Useful extra bits for Python

License:        MIT
URL:            https://github.com/testing-cabal/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/e/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%if %{with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif # with _python2
%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif @ with_python3

%description
%{pypi_name} is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.

%if %{with_python2}
%package -n python2-%{pypi_name}
Summary:        Useful extra bits for Python
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{pypi_name} is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        Useful extra bits for Python
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
%{pypi_name} is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
%if %{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

# Set python2 as build default
#%if %{with_python2}
find -name '*.py' | xargs sed -i '1s|^#!.*python.*|#!%{__python2}|'
#%endif # with_python2

%if %{with_python3}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!.*python.*|#!%{__python3}|'
%endif # with_python3

%build
%if %{with_python2}
%{py2_build}
%endif

%if %{with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install

# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with_python3}
pushd %{py3dir}
%{py3_install}
popd
%endif # with_python3

%if %{with_python2}
%{py2_install}
%endif

%if %{with_python2}
%files -n python2-%{pypi_name}
%doc LICENSE NEWS README.rst
# For noarch packages: sitelib
%{python2_sitelib}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc LICENSE NEWS README.rst
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Wed May 29 2013 Matthias Runge <mrunge@redhat.com> - 0.0.3-2
- spec cleanup and enable tests

* Wed May  1 2013 Michel Salim <salimma@fedoraproject.org> - 0.0.3-1
- Initial package
