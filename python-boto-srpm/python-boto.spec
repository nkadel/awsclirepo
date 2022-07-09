%global pypi_name boto
%global pypi_version 2.49.0

%if 0%{?fedora} || 0%{?rhel} > 8
%bcond_with python2
%else
%bcond_without python2
%endif
%bcond_without python3
%bcond_with unittests

Summary:        A simple, lightweight interface to Amazon Web Services
Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        0%{?dist}
License:        MIT
Group:          Development/Languages
URL:            https://github.com/%{pypi_name}/%{pypi_name}
Source0:        %pypi_source
# Taken from sourcecode 2014-07-31
Source1:        boto-mit-license.txt

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif  # with python3

%if %{with unittests}
%if %{with python2}
BuildRequires:  python2-httpretty
BuildRequires:  python2-mock
BuildRequires:  python2-nose
BuildRequires:  python2-requests
%endif
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-httpretty
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-requests
%endif  # with python3
%endif  # with unittests

%if %{with python2}
Requires:       python2-requests
Requires:       python2-rsa

Provides:       python2-%{pypi_name} = %{version}-%{release}
%endif

BuildArch:      noarch

%description
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.


%if %{with python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        A simple, lightweight interface to Amazon Web Services

Requires:       python%{python3_pkgversion}-requests
%if 0%{?fedora} > 20
# python3-rsa was introduced in python-rsa-3.1.1-6.fc21.
# If it is backported to F20 please file a bug to request a rebuild
# without this condition.
Requires:       python%{python3_pkgversion}-rsa
%endif  # fedora > 20


%description -n python%{python3_pkgversion}-%{pypi_name}
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports over thirty services, such as S3 (Simple Storage Service),
SQS (Simple Queue Service), and EC2 (Elastic Compute Cloud) via their
REST and Query APIs.  The goal of boto is to support the full breadth
and depth of Amazon Web Services.  In addition, boto provides support
for other public services such as Google Storage in addition to private
cloud systems like Eucalyptus, OpenStack and Open Nebula.
%endif  # with python3


%prep
%setup -q -n %{pypi_name}-%{version}
cp -p %{SOURCE1} .

rm -r %{pypi_name}.egg-info

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%if %{with python2}
%{__python2} setup.py build
%endif

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif  # with python3


%install
%if %{with python3}
# Scripts only work with python2
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
rm -f $RPM_BUILD_ROOT/%{_bindir}/*
%endif  # with python3

%if %{with python2}
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
%endif

%check
%if %{with unittests}
%if %{with python2}
%{__python2} tests/test.py default
%endif

%if %{with python3}
pushd %{py3dir}
%{__python3} tests/test.py default
popd
%endif  # with python3
%endif  # with unittests


%if %{with python2}
%files
# For some reason this definition really does have to go in this section.
%{!?_licensedir: %global license %%doc}
%license boto-mit-license.txt
%doc README.rst
%{_bindir}/asadmin
%{_bindir}/bundle_image
%{_bindir}/cfadmin
%{_bindir}/cq
%{_bindir}/cwutil
%{_bindir}/dynamodb_dump
%{_bindir}/dynamodb_load
%{_bindir}/elbadmin
%{_bindir}/fetch_file
%{_bindir}/glacier
%{_bindir}/instance_events
%{_bindir}/kill_instance
%{_bindir}/launch_instance
%{_bindir}/list_instances
%{_bindir}/lss3
%{_bindir}/mturk
%{_bindir}/pyami_sendmail
%{_bindir}/route53
%{_bindir}/s3put
%{_bindir}/sdbadmin
%{_bindir}/taskadmin
%{python2_sitelib}/%{pypi_name}*
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%license boto-mit-license.txt
%{python3_sitelib}/%{pypi_name}*
%endif  # with python3


%changelog
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
