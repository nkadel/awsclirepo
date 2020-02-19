# This is an epel-only package.
# We want python3*-dateutil in EPEL, but the original package is in RHEL.
# This was forked from the latest python-dateutil in rawhide on 2016-07-27.
Name:           python%{python3_pkgversion}-dateutil
Version:        2.4.2
Release:        5%{?dist}
Epoch:          1
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        Python
URL:            https://github.com/dateutil/dateutil
Source0:        https://github.com/dateutil/dateutil/archive/%{version}.tar.gz
# https://github.com/dateutil/dateutil/issues/11
Patch0:         python-dateutil-system-zoneinfo.patch
Patch1:         python-dateutil-timelex-string.patch

BuildArch:      noarch

%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six

Requires:       python%{python3_pkgversion}-six
Requires:       tzdata
%{?python_provide:%python_provide python2-%{pkgname}}

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 3.

#%%package -n python%%{python3_pkgversion}-dateutil
#Summary:        Powerful extensions to the standard datetime module
#BuildRequires:  python%%{python3_pkgversion}-devel
#BuildRequires:  python%%{python3_pkgversion}-setuptools
#BuildRequires:  python%%{python3_pkgversion}-six
#
#Requires:       python%%{python3_pkgversion}-six
#Requires:       tzdata

#%%description -n python%%{python3_pkgversion}-dateutil
#The dateutil module provides powerful extensions to the standard datetime
#module available in Python 2.3+.

#This is the version for Python 3.

%package doc
Summary: API documentation for python-dateutil

%description doc
This package contains %{summary}.

%prep
%autosetup -p0 -n dateutil-%{version}

iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
mv NEWS.new NEWS

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
%{__python3} setup.py test

%files -n python%{python3_pkgversion}-dateutil
%{!?_licensedir:%global license %doc} 
%license LICENSE
%doc NEWS README.rst
%{python3_sitelib}/dateutil/
%{python3_sitelib}/*.egg-info

%changelog
* Mon Apr 29 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1:2.4.2-0
- Discard otherversion

* Thu Mar 07 2019 Troy Dawson <tdawson@redhat.com>
- Rebuilt to change main python from 3.4 to 3.6

* Wed Jan 16 2019 Scott K Logan <logans@cottsay.net> - 1:2.4.2-4
- Support python36 on epel7.

* Thu Jun 25 2015 Ralph Bean <rbean@redhat.com> - 1:2.4.2-3
- Support python34 on epel7.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.2-1
- Update to latest upstream release.

* Tue Mar  3 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-3
- Add patch for string handling in dateutil.tz.tzstr (#1197791)

* Wed Jan 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-2
- Add python3 subpackage.
- Conflict with python-vobject <= 0.8.1c-10 (workaround until #1183377
  is fixed one way or another).

* Wed Jan 21 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.4.0-1
- Change to new upstream, update to 2.4 (#1126521)
- Build documentation.

* Tue Aug 05 2014 Jon Ciesla <limburgher@gmail.com> - 1:1.5-9
- Reverting to 1.5 pre user feedback and upstream.

* Mon Aug 04 2014 Jon Ciesla <limburgher@gmail.com> - 2.2-1
- Update to 2.2, BZ 1126521.
- Fix bad dates.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-3
- Adjust patch to respect systemwide tzdata. Ref bug 729786

* Thu Sep 15 2011 Jef Spaleta <jspaleta@fedoraproject.org> - 1.5-2
- Added a patch to respect systemwide tzdata. Ref bug 729786

* Wed Jul 13 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5-1
- New upstream release
- Fix UTF8 encoding correctly
- Drop buildroot, clean, defattr and use macro for Source

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.4.1-2
- small specfile fix

* Fri Feb 20 2009 Jef Spaleta <jspaleta AT fedoraproject DOT org> - 1.4.1-2
- New upstream version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4-3
- Rebuild for Python 2.6

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-2
- fix license tag

* Tue Jul 01 2008 Jef Spaleta <jspaleta AT fedoraproject DOT org> 1.4-1
- Latest upstream release

* Fri Jan 04 2008 Jef Spaleta <jspaleta@fedoraproject.org> 1.2-2
- Fix for egg-info file creation

* Thu Jun 28 2007 Orion Poplawski <orion@cora.nwra.com> 1.2-1
- Update to 1.2

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 1.1-5
- Fix python-devel BR, as per discussion in maintainers-list

* Mon Dec 11 2006 Jef Spaleta <jspaleta@gmail.com> 1.1-4
- Release bump for rebuild against python 2.5 in devel tree

* Wed Jul 26 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-3
- Add patch to fix building on x86_64

* Wed Feb 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-2
- Rebuild for gcc/glibc changes

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 1.1-1
- Update to 1.1

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 1.0-1
- Update to 1.0

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Initial Fedora Extras package
