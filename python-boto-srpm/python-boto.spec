%bcond_without python3
%bcond_with executables

# Unit tests don't work on python 2.6
%if 0%{?el6}
%bcond_with unittests
%else
%bcond_without unittests
%endif


Summary:        A simple, lightweight interface to Amazon Web Services
Name:           python-boto
Version:        2.45.0
Release:        0%{?dist}
License:        MIT
Group:          Development/Languages
URL:            https://github.com/boto/boto
Source0:        https://pypi.io/packages/source/b/boto/boto-%{version}.tar.gz
# Taken from sourcecode 2014-07-31
Source1:        boto-mit-license.txt

# Unbundle python-six
# https://github.com/boto/boto/pull/3086
Patch1:         boto-2.39.0-devendor.patch

# Add NAT gateway support
# https://github.com/boto/boto/pull/3472
Patch2:         boto-2.40.0-nat-gateway.patch

# Fix max_retry_delay config option
# https://github.com/boto/boto/pull/3506
# https://github.com/boto/boto/pull/3508
Patch4:         boto-2.40.0-retry-float.patch

# Add aws-exec-read to S3's canned ACL list
# https://github.com/boto/boto/pull/3332
Patch5:         boto-2.40.0-aws-exec-read.patch

# Add new instance attributes
# https://github.com/boto/boto/pull/3077
# https://github.com/boto/boto/pull/3131
Patch6:         boto-2.40.0-instance-attributes.patch

# Fix multi-VPC hosted zone parsing
# https://github.com/boto/boto/pull/2882
Patch7:         boto-2.40.0-multi-vpc-zone.patch

# Fix request logging for S3 requests
# https://github.com/boto/boto/issues/2722
# https://github.com/boto/boto/pull/2875
Patch8:         boto-2.40.0-s3-requestlog.patch

# Allow route53 health check resource paths to be none
# https://github.com/boto/boto/pull/2866
Patch9:         boto-2.40.0-route53-no-resourcepath.patch

# Add ModifySubnetAttribute support
# https://github.com/boto/boto/pull/3111
Patch10:        boto-2.45.0-modifysubnetattribute.patch

%if 0%{?rhel} == 6
Buildrequires:  epel-rpm-macros
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
%endif  # with python3

%if %{with unittests}
BuildRequires:  python2-httpretty
BuildRequires:  python2-mock
BuildRequires:  python2-nose
BuildRequires:  python2-requests
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-httpretty
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-requests
%endif  # with python3
%endif  # with unittests

BuildArch:      noarch


%description
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.


%package -n python2-boto
Summary:        A simple, lightweight interface to Amazon Web Services

Requires:       python2-requests
Requires:       python2-rsa
Requires:       python2-six >= 1.7

Provides:       python2-boto = %{version}-%{release}
Obsoletes:      python2-boto < 2.39


%description -n python2-boto
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.


%if %{with python3}
%package -n python%{python3_pkgversion}-boto
Summary:        A simple, lightweight interface to Amazon Web Services

Requires:       python%{python3_pkgversion}-requests
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-rsa


%description -n python%{python3_pkgversion}-boto
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.
%endif  # with python3


%prep
%autosetup -p1 -n boto-%{version}

rm -r boto/vendored

cp -p %{SOURCE1} .


%build
%{__python2} setup.py build
%if %{with python3}
%{__python3} setup.py build
%endif  # with python3


%install
%if %{with python3}
# Scripts only work with python2
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_bindir}/*
%endif  # with python3

%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if %{without executables}
# Make executables doc files instead
chmod -x $RPM_BUILD_ROOT/%{_bindir}/*
mv $RPM_BUILD_ROOT/%{_bindir} examples
%endif


%check
%if %{with unittests}
%{__python2} tests/test.py default
%if %{with python3}
%{__python3} tests/test.py default
%endif  # with python3
%endif  # with unittests


%files -n python2-boto
%license boto-mit-license.txt
%doc README.rst
%{python2_sitelib}/boto*

%if %{with executables}
%{_bindir}/*
%else
%doc examples
%endif


%if %{with python3}
%files -n python%{python3_pkgversion}-boto
%license boto-mit-license.txt
%{python3_sitelib}/boto*
%endif  # with python3


%changelog
* Fri Jan 27 2017 Garrett Holmstrom <gholms@fedoraproject.org> - 2.45.0-3
- Added support for ModifySubnetAttribute

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.45.0-2
- Rebuild for Python 3.6

* Thu Dec 15 2016 Jon Ciesla <limburgher@gmail.com> - 2.45.0-1
- 2.40.0.

* Fri Dec  9 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.44.0-1
- Updated to 2.44.0 (RH #1403362)

* Tue Oct 25 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.43.0-1
- Updated to 2.43.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul  5 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.41.0-1
- Updated to 2.41.0

* Tue Jun 21 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.40.0-2
- Cleaned up spec file
- Added NAT gateway support
- Fixed sigv4 protocol selection
- Fixed max_retry_delay config option
- Added aws-exec-read to S3's canned ACL list
- Added new instance attributes
- Fixed multi-VPC hosted zone parsing
- Fixed request logging for S3 requests
- Allowed route53 health check resource paths to be none

* Mon May 23 2016 Jon Ciesla <limburgher@gmail.com> - 2.40.0-1
- 2.40.0.
- Kinesis patch upstreamed.

* Fri Jan 29 2016 Garrett Holmstrom <gholms@fedoraproject.org> - 2.39.0-1
- Updated to 2.39.0 (RH #1300424)
- Switched to systemwide copy of python-six on el7
- Enabled unit tests on el7
- Renamed python-boto to python2-boto to comply with current python
  packaging standards

* Mon Nov 30 2015 Ryan S. Brown <sb@ryansb.com> - 2.38.0-5
- Add patch for unittest failure https://github.com/boto/boto/pull/3412

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Garrett Holmstrom <gholms@fedoraproject.org> - 2.38.0-2
- Fixed ImportErrors on RHEL 7 (RH #1229863)

* Fri Apr 10 2015 Garrett Holmstrom <gholms@fedoraproject.org> - 2.38.0-1
- Updated to 2.38.0
- Added BuildRequires for python-six
- Made sample executables doc files in F23

* Wed Apr  8 2015 Garrett Holmstrom <gholms@fedoraproject.org> - 2.37.0-1
- Updated to 2.37.0 (RH #1180861)
- Dropped executables in F23
- Unbundled python-six (boto #3086)
- Enabled unit tests on Fedora (RH #1072946)

* Sun Nov  9 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-4
- Fixed python3 requires

* Fri Nov  7 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-3
- Re-fix executables (RH #1152444)

* Fri Nov  7 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-2
- Added missing python-requests and python-rsa dependencies
- Disabled unit tests due to rawhide/F21 python regression (RH #1161166:c4)

* Fri Nov  7 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.34.0-1
- Updated to 2.34.0 (RH #1072925, RH #1072928, RH #1161229)
- Made executables point to python2 (RH #1152444)
- Enabled unit tests on Fedora (RH #1072946)

* Thu Aug 21 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.32.1-1
- Updated to 2.32.1 (RH #1126056, RH #1132348)
- Added python3-boto (RH #1024363)
- Added (but did not enable) unit tests (RH #1072946, RH #1072923)

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.27.0-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 21 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.27.0-1
- Updated to 2.27.0

* Wed Feb 12 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.25.0-2
- Fixed roboto parameter type conversion (boto #2094, RH #1064550)

* Mon Feb 10 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.25.0-1
- Updated to 2.25.0
- This update makes s3.get_bucket use HEAD instead of GET

* Mon Jan 20 2014 Garrett Holmstrom <gholms@fedoraproject.org> - 2.23.0-1
- Updated to 2.23.0
- Fixed auth for anonymous S3 requests (boto #1988)

* Thu Sep 26 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.13.3-1
- Updated to 2.13.3
- Note that this version changes register_image's virtualization_type parameter
- Fixed auto-scaling PropagateAtLaunch parsing (#1011682)

* Mon Jul 29 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.9.9-2
- Re-fixed autoscaling policy parsing (boto #1538)

* Thu Jul 25 2013 Orion Poplawski <orion@cora.nwra.com> - 2.9.9-1
- Update to 2.9.9

* Fri Jun 21 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.9.6-2
- Rebuilt after merge

* Fri Jun 21 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.9.6-1
- Updated to 2.9.6
- Fixed autoscaling policy parsing (boto #1538)

* Thu May  9 2013 Orion Poplawski <orion@cora.nwra.com> - 2.9.2-1
- Update to 2.9.2 (bug #948714)
- Spec cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.2-3
- Fixed parsing of current/previous instance state data (boto #881)

* Wed Nov 21 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.6.0-2
- Updated to 2.6.0 (#876517)
- Note that this version enables SSL cert verification by default.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.2-1
- Updated to 2.5.2
- Fixed failure when metadata is empty (#838076)

* Thu Jun 14 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.1-1
- Updated to 2.5.1 (last-minute upstream bugfix)

* Wed Jun 13 2012 Garrett Holmstrom <gholms@fedoraproject.org> - 2.5.0-1
- Updated to 2.5.0 (#828912)

* Wed Mar 21 2012 Robert Scheck <robert@fedoraproject.org> 2.3.0-1
- Upgrade to 2.3.0 (#786301 #c10)

* Tue Mar 13 2012 Robert Scheck <robert@fedoraproject.org> 2.2.2-1
- Upgrade to 2.2.2 (#786301, thanks to Bobby Powers)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Robert Scheck <robert@fedoraproject.org> 2.0-1
- Upgrade to 2.0 (#723088)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9b-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Robert Scheck <robert@fedoraproject.org> 1.9b-6
- Added a patch for python 2.4 support (#656446, #661233)

* Thu Dec 02 2010 Lubomir Rintel <lubo.rintel@gooddata.com> 1.9b-5
- Apply a patch for python 2.7 support (#659248)

* Thu Nov 18 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-4
- Added patch to fix parameter of build_list_params() (#647005)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.9b-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Feb 09 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-2
- Backported upstream patch for image registration (#561216)

* Sat Jan 09 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-1
- Upgrade to 1.9b

* Fri Jul 24 2009 Robert Scheck <robert@fedoraproject.org> 1.8d-1
- Upgrade to 1.8d (#513560)

* Wed Jun 03 2009 Luke Macken <lmacken@redhat.com> 1.7a-2
- Add python-setuptools-devel to our build requirements, for egg-info

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> 1.7a-1
- Upgrade to 1.7a

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.5c-2
- Rebuild against rpm 4.6

* Sun Dec 07 2008 Robert Scheck <robert@fedoraproject.org> 1.5c-1
- Upgrade to 1.5c

* Fri Dec 05 2008 Jeremy Katz <katzj@redhat.com> 1.2a-2
- Rebuild for python 2.6

* Wed May 07 2008 Robert Scheck <robert@fedoraproject.org> 1.2a-1
- Upgrade to 1.2a

* Sat Feb 09 2008 Robert Scheck <robert@fedoraproject.org> 1.0a-1
- Upgrade to 1.0a

* Sat Dec 08 2007 Robert Scheck <robert@fedoraproject.org> 0.9d-1
- Upgrade to 0.9d

* Thu Aug 30 2007 Robert Scheck <robert@fedoraproject.org> 0.9b-1
- Upgrade to 0.9b
- Initial spec file for Fedora and Red Hat Enterprise Linux
