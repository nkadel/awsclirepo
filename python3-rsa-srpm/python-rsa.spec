%global pypi_name rsa

%if 0%{?rhel}
%global with_python3 0
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}
%else
%global with_python3 1
%endif

Name:           python-%{pypi_name}
Version:        3.4.1
Release:        1%{?dist}
Summary:        Pure-Python RSA implementation

License:        ASL 2.0
URL:            http://stuvel.eu/rsa
Source0:        https://pypi.python.org/packages/source/r/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pyasn1%{!?el6: >= 0.1.3}
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pyasn1 >= 0.1.3
BuildRequires:  python3-unittest2
%endif # with_python3

%description
Python-RSA is a pure-Python RSA implementation. It supports encryption
and decryption, signing and verifying signatures, and key generation
according to PKCS#1 version 1.5. It can be used as a Python library as
well as on the command-line.

%package -n     python2-%{pypi_name}
Summary:        Pure-Python RSA implementation
%{?python_provide:%python_provide python2-%{pypi_name}}
%{?el6:Provides: python-%{pypi_name}}
%{?el6:Obsoletes: python-%{pypi_name} < 3.3}

Requires:       python-pyasn1%{!?el6: >= 0.1.3}
Requires:       python-setuptools
%description -n python2-%{pypi_name}
Python-RSA is a pure-Python RSA implementation. It supports encryption
and decryption, signing and verifying signatures, and key generation
according to PKCS#1 version 1.5. It can be used as a Python library as
well as on the command-line.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Pure-Python RSA implementation
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-pyasn1 >= 0.1.3
Requires:       python3-setuptools
%description -n python3-%{pypi_name}
Python-RSA is a pure-Python RSA implementation. It supports encryption
and decryption, signing and verifying signatures, and key generation
according to PKCS#1 version 1.5. It can be used as a Python library as
well as on the command-line.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
# This is a dirty workaround for EL6
%{?el6:rm -rf %{pypi_name}.egg-info}
%{?el6:sed -i "s/pyasn1 >= 0.1.3/pyasn1 >= 0/" setup.py}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%py2_install
cp %{buildroot}%{_bindir}/pyrsa-priv2pub %{buildroot}%{_bindir}/pyrsa-priv2pub-2
cp %{buildroot}%{_bindir}/pyrsa-keygen %{buildroot}%{_bindir}/pyrsa-keygen-2
cp %{buildroot}%{_bindir}/pyrsa-encrypt %{buildroot}%{_bindir}/pyrsa-encrypt-2
cp %{buildroot}%{_bindir}/pyrsa-decrypt %{buildroot}%{_bindir}/pyrsa-decrypt-2
cp %{buildroot}%{_bindir}/pyrsa-sign %{buildroot}%{_bindir}/pyrsa-sign-2
cp %{buildroot}%{_bindir}/pyrsa-verify %{buildroot}%{_bindir}/pyrsa-verify-2
cp %{buildroot}%{_bindir}/pyrsa-encrypt-bigfile %{buildroot}%{_bindir}/pyrsa-encrypt-bigfile-2
cp %{buildroot}%{_bindir}/pyrsa-decrypt-bigfile %{buildroot}%{_bindir}/pyrsa-decrypt-bigfile-2

%if 0%{?with_python3}
%py3_install
cp %{buildroot}%{_bindir}/pyrsa-priv2pub %{buildroot}%{_bindir}/pyrsa-priv2pub-3
cp %{buildroot}%{_bindir}/pyrsa-keygen %{buildroot}%{_bindir}/pyrsa-keygen-3
cp %{buildroot}%{_bindir}/pyrsa-encrypt %{buildroot}%{_bindir}/pyrsa-encrypt-3
cp %{buildroot}%{_bindir}/pyrsa-decrypt %{buildroot}%{_bindir}/pyrsa-decrypt-3
cp %{buildroot}%{_bindir}/pyrsa-sign %{buildroot}%{_bindir}/pyrsa-sign-3
cp %{buildroot}%{_bindir}/pyrsa-verify %{buildroot}%{_bindir}/pyrsa-verify-3
cp %{buildroot}%{_bindir}/pyrsa-encrypt-bigfile %{buildroot}%{_bindir}/pyrsa-encrypt-bigfile-3
cp %{buildroot}%{_bindir}/pyrsa-decrypt-bigfile %{buildroot}%{_bindir}/pyrsa-decrypt-bigfile-3
%endif # with_python3

%files -n python2-%{pypi_name}
%{!?_licensedir:%global license %doc}
%doc README.md
%license LICENSE
%if 0%{?with_python3} == 0
%{_bindir}/pyrsa-priv2pub
%{_bindir}/pyrsa-keygen
%{_bindir}/pyrsa-encrypt
%{_bindir}/pyrsa-decrypt
%{_bindir}/pyrsa-sign
%{_bindir}/pyrsa-verify
%{_bindir}/pyrsa-encrypt-bigfile
%{_bindir}/pyrsa-decrypt-bigfile
%endif # with_python3
%{_bindir}/pyrsa-priv2pub-2
%{_bindir}/pyrsa-keygen-2
%{_bindir}/pyrsa-encrypt-2
%{_bindir}/pyrsa-decrypt-2
%{_bindir}/pyrsa-sign-2
%{_bindir}/pyrsa-verify-2
%{_bindir}/pyrsa-encrypt-bigfile-2
%{_bindir}/pyrsa-decrypt-bigfile-2
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{_bindir}/pyrsa-priv2pub
%{_bindir}/pyrsa-keygen
%{_bindir}/pyrsa-encrypt
%{_bindir}/pyrsa-decrypt
%{_bindir}/pyrsa-sign
%{_bindir}/pyrsa-verify
%{_bindir}/pyrsa-encrypt-bigfile
%{_bindir}/pyrsa-decrypt-bigfile
%{_bindir}/pyrsa-priv2pub-3
%{_bindir}/pyrsa-keygen-3
%{_bindir}/pyrsa-encrypt-3
%{_bindir}/pyrsa-decrypt-3
%{_bindir}/pyrsa-sign-3
%{_bindir}/pyrsa-verify-3
%{_bindir}/pyrsa-encrypt-bigfile-3
%{_bindir}/pyrsa-decrypt-bigfile-3
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif # with_python3

%changelog
* Sat Mar 26 2016 Fabio Alessandro Locati <fabio@locati.cc> - 3.4.1-1
- Update to 3.4.1

* Fri Mar 18 2016 Fabio Alessandro Locati <fabio@locati.cc> - 3.4-1
- Bump to 3.4
- Remove the patch that is no longer needed since it has been merged upstream

* Tue Feb 09 2016 Fabio Alessandro Locati <fabio@locati.cc> - 3.3-5
- Fix bug #1305644

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Fabio Alessandro Locati <fabio@locati.cc> - 3.3-3
- Fix bug #1303660

* Wed Jan 13 2016 Fabio Alessandro Locati <fabio@locati.cc> - 3.3-2
- Fix for EL6 and EPEL7

* Wed Jan 13 2016 Fabio Alessandro Locati <fabio@locati.cc> - 3.3-1
- Update to current upstream
- Fix CVE-2016-1494
- Bring spec compliant with current policy

* Tue Dec  8 2015 Paul Howarth <paul@city-fan.org> - 3.1.4-3
- Fix FTBFS (Debian Bug #804430)
- Run the tests for both python2 and python3

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Oct 13 2015 Paul Howarth <paul@city-fan.org> - 3.1.4-1
- Update to 3.1.4 (#1226667)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.1.1-6
- Add Python 3 subpackage

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-4
- Fix build in F20
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-2
- Change license name, remove MANIFEST.in

* Sun May 19 2013 Yohan Graterol <yohangraterol92@gmail.com> - 3.1.1-1
- Initial packaging
