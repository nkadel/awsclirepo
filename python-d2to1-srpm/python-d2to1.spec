%global with_python3 1
%global with_python2 1

%global pypi_name d2to1

Name: python-%{pypi_name}
Version: 0.2.10
#Release: 1%%{?dist}
Release: 0%{?dist}
Summary: Allows using distutils2-like setup.cfg files with setup.py
License: BSD

Group: Development/Languages
URL: https://pypi.python.org/pypi/d2to1
Source0: https://pypi.python.org/packages/source/d/d2to1/%{pypi_name}-%{version}.tar.gz
BuildRequires: openssl-devel

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

BuildRequires: python2-devel
BuildRequires: python2-setuptools
Requires: python2-setuptools
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildArch: noarch

%description
d2to1 allows using distutils2-like setup.cfg files for a package's metadata 
with a distribute/setuptools setup.py script. It works by providing a 
distutils2-formatted setup.cfg file containing all of a package's metadata, 
and a very minimal setup.py which will slurp its arguments from the setup.cfg.

%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-d2to1
Summary: Allows using distutils2-like setup.cfg files with setup.py
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
Requires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-d2to1
d2to1 allows using distutils2-like setup.cfg files for a package's metadata 
with a distribute/setuptools setup.py script. It works by providing a 
distutils2-formatted setup.cfg file containing all of a package's metadata, 
and a very minimal setup.py which will slurp its arguments from the setup.cfg.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info


for file in \
    distribute_setup.py \
    d2to1/tests/testpackage/distribute_setup.py \
    d2to1/tests/testpackage/README.txt; do
    echo Correct http://pypi.python.org in $file
    sed -i.bak  's|http://pypi.python.org/|https://pypi.python.org/|g' $file
done

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%if 0%{?with_python2}
# updates obsolete .py files for python2
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'
%endif # with_python2

%build
%if 0%{?with_python2}
%{__python2} setup.py build
%endif # with_python2

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root  %{buildroot}
popd
%endif # with_python3

%if 0%{?with_python2}
%{__python2} setup.py install -O1 --skip-build --root  %{buildroot}
%endif

%files
%doc CHANGES.rst CONTRIBUTORS LICENSE README.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-d2to1
%doc CHANGES.rst CONTRIBUTORS LICENSE README.rst
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 0.2.10-0
- Enable python3 by default, use python3_pkgversion
- Change URL for downloaded distribute module to use https://

* Thu Apr 25 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.10-1
- New upstream source

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.7-2
- Requires for python3 inside python3 package (bz #891381)

* Wed Sep 26 2012 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.7-1
- New upstream source
- Removing upstream egg-info and defattr

* Thu Sep 22 2011 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.5-1
- Initial spec file

