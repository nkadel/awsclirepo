%global with_python3 1
%global with_python2 0

Name:           python-extras
Version:        0.0.3
#Release:        2%%{?dist}
Release:        0%{?dist}
Summary:        Useful extra bits for Python

License:        MIT
URL:            https://github.com/testing-cabal/extras
Source0:        https://pypi.python.org/packages/source/e/extras/extras-%{version}.tar.gz

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
extras is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.

%if %{with_python2}
%package -n python2-extras
Summary:        Useful extra bits for Python

%description -n python2-extras
extras is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-extras
Summary:        Useful extra bits for Python

%description -n python%{python3_pkgversion}-extras
extras is a set of extensions to the Python standard library, originally
written to make the code within testtools cleaner, but now split out for
general use outside of a testing context.
%endif # with_python3

%prep
%setup -q -n extras-%{version}
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
%files -n python2-extras
%doc LICENSE NEWS README.rst
# For noarch packages: sitelib
%{python2_sitelib}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-extras
%doc LICENSE NEWS README.rst
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Wed May 29 2013 Matthias Runge <mrunge@redhat.com> - 0.0.3-2
- spec cleanup and enable tests

* Wed May  1 2013 Michel Salim <salimma@fedoraproject.org> - 0.0.3-1
- Initial package
