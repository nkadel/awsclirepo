# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global with_python3 1

%global with_python2 1
%if 0%{?fedora} > 30
%global with_python2 0
%endif

%global pypi_name PyYAML

#Name:           PyYAML
Name:           python-%{pypi_name}
Version:        3.10
#Release:        11%%{?dist}
Release:        0%{?dist}
Summary:        YAML parser and emitter for Python

Group:          Development/Libraries
License:        MIT
URL:            http://pyyaml.org/
Source0:        http://pyyaml.org/download/pyyaml/%{pypi_name}-%{version}.tar.gz
BuildRequires:  libyaml-devel

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%if %{with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if 0%{?rhel} && 0%{?rhel} < 8
BuildRequires:  Cython
%else
BuildRequires:  python2-Cython
%endif
%endif # with_python2
%if %{with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-Cython
%endif # with_python3

# http://pyyaml.org/ticket/247
Patch0: PyYAML-size_t_not_int.patch

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%if %{with_python2}
%package -n python2-%{pypi_name}
Summary: YAML parser and emitter for Python
Group: Development/Libraries
#Provides:       python2-yaml = %%{version}-%%{release}
#Provides:       python2-yaml%%{?_isa} = %%{version}-%%{release}
%{?python_provide:%python_provide python2-yaml}
# Due to misnaming as "PyYAML" in RHEL
Provides: PyYAML = %{version}-%{release}
Conflicts: PyYAML

%description -n python2-%{pypi_name}
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary: YAML parser and emitter for Python
Group: Development/Libraries
#Provides:       python%%{python3_pkgversion}-yaml = %%{version}-%%{release}
#Provides:       python%%{python3_pkgversion}-yaml%%{?_isa} = %%{version}-%%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-yaml}

%description -n python%{python3_pkgversion}-%{pypi_name}
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.
%endif # with_python3

%prep
%setup -q -n %{pypi_name}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py
%patch0 -p1
pushd ext
cython _yaml.pyx
popd

%if %{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if %{with_python2}
CFLAGS="${RPM_OPT_FLAGS}" %{__python2} setup.py --with-libyaml build
%endif # with_python2

%if %{with_python3}
pushd %{py3dir}
CFLAGS="${RPM_OPT_FLAGS}" %{__python3} setup.py --with-libyaml build
popd
%endif

%install
%if %{with_python2}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%endif # with_python2

%if %{with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif

%check
%if %{with_python2}
%{__python} setup.py test
%endif

%if %{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%%clean
rm -rf %{buildroot}

%if %{with_python2}
%files -n python2-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python2_sitearch}/*
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES LICENSE PKG-INFO README examples
%{python3_sitearch}/*
%endif # with_python3


%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 3.10-0
- Split to python2-PyYAML and python34-PyYAML, blocking PyYAML

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.10-11
- Mass rebuild 2014-01-24

* Tue Jan  7 2014 John Eckersberg <jeckersb@redhat.com> - 3.10-10
- Add patch to fix build issue on s390x (bz1048898)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.10-9
- Mass rebuild 2013-12-27

* Thu Aug  8 2013 John Eckersberg <jeckersb@redhat.com> - 3.10-8
- Add check section and run test suite

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.10-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Wed Aug  1 2012 David Malcolm <dmalcolm@redhat.com> - 3.10-5
- remove rhel logic from with_python3 conditional

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 John Eckersberg <jeckersb@redhat.com> - 3.10-3
- Add Provides for python-yaml (BZ#740390)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 John Eckersberg <jeckersb@redhat.com> - 3.10-1
- New upstream release 3.10

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 John Eckersberg <jeckersb@redhat.com> - 3.09-7
- Add support to build for python 3

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3.09-6
- Bump release number for upgrade path

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.09-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Oct 02 2009 John Eckersberg <jeckersb@redhat.com> - 3.09-1
- New upstream release 3.09

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 - John Eckersberg <jeckersb@redhat.com> - 3.08-5
- Minor tweaks to spec file aligning with latest Fedora packaging guidelines
- Enforce inclusion of libyaml in build with --with-libyaml option to setup.py
- Deliver to %%{python_sitearch} instead of %%{python_sitelib} due to _yaml.so
- Thanks to Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-4
- Correction, change libyaml to libyaml-devel in BuildRequires

* Mon Mar 2 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-3
- Add libyaml to BuildRequires

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 John Eckersberg <jeckersb@redhat.com> - 3.08-1
- New upstream release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.06-2
- Rebuild for Python 2.6

* Fri Oct 24 2008 John Eckersberg <jeckersb@redhat.com> - 3.06-1
- New upstream release

* Wed Jan 02 2008 John Eckersberg <jeckersb@redhat.com> - 3.05-2
- Remove explicit dependency on python >= 2.3
- Remove executable on example script in docs

* Mon Dec 17 2007 John Eckersberg <jeckersb@redhat.com> - 3.05-1
- Initial packaging for Fedora
