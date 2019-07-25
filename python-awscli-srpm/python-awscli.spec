# python3_pkgversion macro for EPEL in older RHEL
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global pypi_name awscli

%{?python_enable_dependency_generator}

#%%if 0%%{?rhel} && 0%%{?rhel} <= 8
#%%bcond_with python3
#%%else
#%%bcond_without python3
#%%endif
# Build only for python3 to resolve dependencies
%bcond_without python3

%global botocore_version 1.12.188

Name:           python-%{pypi_name}
Version:        1.16.198
Release:        1%{?dist}
Summary:        Universal Command Line Environment for AWS

License:        ASL 2.0 and MIT
URL:            http://aws.amazon.com/cli
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Patch0:         relax-dependencies.patch
BuildArch:      noarch
%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{undefined __pythondist_requires}
Requires:       python%{python3_pkgversion}-botocore = %{botocore_version}
Requires:       python%{python3_pkgversion}-colorama >= 0.2.5
Requires:       python%{python3_pkgversion}-docutils >= 0.10
Requires:       python%{python3_pkgversion}-rsa >= 3.1.2
Requires:       python%{python3_pkgversion}-s3transfer >= 0.1.9
Requires:       python%{python3_pkgversion}-PyYAML >= 3.10
%endif
%else
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{undefined __pythondist_requires}
Requires:       python2-botocore = %{botocore_version}
Requires:       python-colorama >= 0.2.5
Requires:       python-docutils >= 0.10
Requires:       python2-rsa >= 3.1.2
Requires:       python2-s3transfer >= 0.1.9
Requires:       PyYAML >= 3.10
%endif
%endif # with python3
%if ! (0%{?rhel} && 0%{?rhel} <= 7)
Recommends:     bash-completion
Recommends:     zsh
Recommends:     groff
%endif # Fedora

%if %{with python3}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
%else
%{?python_provide:%python_provide python2-%{pypi_name}}
%endif # with python3
# Block and obsolete misnamed awscli package
Provides: awscli = %{version}-%{release}
Obsoletes: awscli <= %{version}-%{release}
Conflicts: awscli

%description
This package provides a unified
command line interface to Amazon Web Services.

%prep
%autosetup -n %{pypi_name}-%{version} -p 1
rm -rf %{pypi_name}.egg-info

%build
%if %{with python3}
%py3_build
%else
%py2_build
%endif # with python3

%install
%if %{with python3}
%py3_install
%else
%py2_install
%endif # with python3
# Fix path and permissions for bash completition
%global bash_completion_dir /etc/bash_completion.d
mkdir -p %{buildroot}%{bash_completion_dir}
mv %{buildroot}%{_bindir}/aws_bash_completer %{buildroot}%{bash_completion_dir}
chmod 644 %{buildroot}%{bash_completion_dir}/aws_bash_completer
# Fix path and permissions for zsh completition
%global zsh_completion_dir /usr/share/zsh/site-functions
mkdir -p %{buildroot}%{zsh_completion_dir}
mv %{buildroot}%{_bindir}/aws_zsh_completer.sh %{buildroot}%{zsh_completion_dir}
chmod 755 %{buildroot}%{zsh_completion_dir}/aws_zsh_completer.sh
ls -alh %{buildroot}%{zsh_completion_dir}/aws_zsh_completer.sh
# We do not need the Windows CMD script
rm %{buildroot}%{_bindir}/aws.cmd

%files
%doc README.rst
%license LICENSE.txt
%{_bindir}/aws
%{_bindir}/aws_completer
%dir %{bash_completion_dir}
%{bash_completion_dir}/aws_bash_completer
%dir %{zsh_completion_dir}
%{zsh_completion_dir}/aws_zsh_completer.sh
%if %{with python3}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%else
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with python3

%changelog
* Thu Jul 25 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.16.198-0
- Backport to RHEL 7

* Sat Jul 13 2019 David Duncan <davdunc@amazon.com> - 1.16.198-1
- Update to 1.16.198
- Add updates and fixes

* Tue May 28 2019 David Duncan <davdunc@amazon.com> - 1.16.167-1
- Update to 1.16.167
- Add updates and fixes

* Wed Apr 24 2019 David Duncan <davdunc@amazon.com> - 1.16.145-1
- Adding support for ap-east-1 

* Thu Mar 21 2019 David Duncan <davdunc@amazon.com> - 1.16.129-1
- Bumping version to 1.16.129

* Sat Feb 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.16.111-1
- Update to 1.16.111

* Mon Feb 11 2019 David Duncan <davdunc@amazon.com> - 1.16.101
- api-change:ecs: Update ecs command to latest version
- api-change:discovery: Update discovery command to latest version
- api-change:dlm: Update dlm command to latest version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.16.85-2
- Enable python dependency generator

* Mon Nov 19 2018 David Duncan <davdunc@amazon.com> - 1.16.57-1
- Update to 1.16.57. Fixes bug #1613078

* Tue Nov 06 2018 Carl George <carl@george.computer> - 1.16.28-3
- Add patch0 to relax dependencies

* Wed Oct 17 2018 Justin W. Flory <jflory7@fedoraproject.org> - 1.16.28-2
- Add groff dependency, fix 'aws help' issue in stock install

* Sun Oct 07 2018 David Duncan <davdunc@amazon.com> - 1.16.28
- Update to 1.16.28

* Sun Sep 02 2018 David Duncan <davdunc@amazon.com> - 1.15.72-1
- Update to 1.15.72. Updates bug #1613078

* Sun Aug 05 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.71-1
- Update to 1.15.71. Fixes bug #1612393

* Fri Aug 03 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.70-1
- Update to 1.15.70. Fixes bug #1611853

* Wed Aug 01 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.69-1
- Update to 1.15.69. Fixes bug #1610059

* Fri Jul 27 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.66-1
- Update to 1.15.66. Fixes bug #1609074

* Thu Jul 26 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.65-1
- Update to 1.15.65. Fixes bug #1608097

* Sun Jul 22 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.63-1
- Update to 1.15.63. Fixes bug #1606924

* Thu Jul 19 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.62-1
- Update to 1.15.62. Fixes bug #1602972

* Wed Jul 18 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.60-1
- Update to 1.15.60. Fixes bug #1602176

* Sun Jul 15 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.59-1
- Update to 1.15.59. Fixes bug #1599467

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.53-1
- Update to 1.15.53. Fixes bug #1598936

* Thu Jul 05 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.52-1
- Update to 1.15.52. Fixes bug #1598597

* Wed Jul 04 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.51-2
- Update to 1.15.51. Fixes bug #1596663

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.48-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.48-1
- Update to 1.14.48. Fixes bug #1596420

* Thu Jun 28 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.47-1
- Update to 1.14.47. Fixes bug #1595469

* Sat Jun 23 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.45-1
- Update to 1.14.45. Fixes bug #1594465

* Fri Jun 22 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.44-1
- Update to 1.14.44. Fixes bug #1594038

* Fri Jun 22 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.43-1
- Update to 1.14.43. Fixes bug #1594038
- Fix python-botocore version to match new python-botocore.

* Wed Jun 20 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.42-1
- Update to 1.14.42. Fixes bug #1593483

* Wed Jun 20 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.41-1
- Update to 1.15.41. Fixes bug #1593040

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.40-2
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.40-1
- Update to 1.15.40. Fixes bug #1591986

* Fri Jun 15 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.39-1
- Update to 1.15.39. Fixes bug #1591048

* Tue Jun 12 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.37-1
- Update to 1.15.37. Fixes bug #1590039

* Sat Jun 09 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.35-1
- Update to 1.15.35. Fixes bug #1588851

* Wed Jun 06 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.33-1
- Update to 1.15.33. Fixes bug #1586055

* Sun Jun 03 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.31-1
- Update to 1.15.31. Fixes bug #1583867

* Sun May 27 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.28-1
- Update to 1.15.28. Fixes bug #1580992

* Fri May 18 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.24-1
- Update to 1.15.24. Fixes bug #1579995

* Fri May 18 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.23-1
- Update to 1.15.23. Fixes bug #1579573

* Wed May 16 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.22-1
- Update to 1.15.22. Fixes bug #1579086

* Wed May 16 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.21-1
- Update to 1.15.21. Fixes bug #1578162

* Fri May 11 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.19-1
- Update to 1.15.19. Fixes bug #1574745

* Wed May 02 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.12-1
- Update to 1.15.12. Fixes bug #1574052

* Fri Apr 27 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.10-1
- Update to 1.15.10. Fixes bug #1572396

* Thu Apr 26 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.9-1
- Update to 1.15.9. Fixes bug #1571002

* Mon Apr 23 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.6-1
- Update to 1.15.6. Fixes bug #1570216

* Fri Apr 20 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.5-1
- Update to 1.15.5. Fixes bug #1569974

* Sat Apr 14 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.4-1
- Update to 1.15.4. Fixes bug #1565379

* Sat Apr 07 2018 Kevin Fenzi <kevin@scrye.com>  - 1.15.2-1
- Update to 1.15.2. Fixes bug #1563195

* Sat Mar 31 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.68-1
- Update to 1.4.68. Fixes bug #1561240

* Tue Mar 27 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.64-1
- Update to 1.4.64. Fixes bug #1560762

* Sun Mar 25 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.63-1
- Update to 1.4.63. Fixes bug #1559367

* Fri Mar 23 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.62-1
- Update to 1.4.62. Fixes bug #1559367

* Wed Mar 21 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.60-1
- Update to 1.4.60. Fixes bug #1559193

* Wed Mar 21 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.59-1
- Update to 1.4.59. Fixes bug #1558758

* Sat Mar 17 2018 Kevin Fenzi <kevin@scrye.com>  - 1.14.58-1
- Update to 1.4.58. Fixes bug #1555085

* Tue Mar 13 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.55-1
- Update to 1.4.55. Fixes bug #1555085

* Tue Mar 13 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.54-1
- Update to 1.14.54. Fixes bug #1554552

* Thu Mar 08 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.53-1
- Update to 1.14.53. Fixes bug 1552345

* Sat Mar 03 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.50-2
- Update for new python-botocore.

* Sat Mar 03 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.50-1
- Update to 1.14.50. Fixes bug #1550746

* Thu Mar 01 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.49-1
- Update to 1.14.49. Fixes bug #1549549

* Sat Feb 24 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.46-1
- Update to 1.14.46. Fixes bug #1546901

* Sat Feb 17 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.41-1
- Update to 1.14.41. Fixes bug #1546437

* Fri Feb 16 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.40-1
- Update to 1.14.40. Fixes bug #1544045

* Thu Feb 08 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.34-1
- Update to 1.14.34. Fixes bug #1543659

* Wed Feb 07 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.33-1
- Update to 1.14.33. Fixes bug #1542468

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.32-2
- Fix python-botocore version requirement.

* Wed Jan 31 2018 Kevin Fenzi <kevin@scrye.com> - 1.14.32-1
- Update to 1.14.32. Fixes bug #1481464

* Sun Aug 13 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.133-1
- Update to 1.11.133

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.109-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.109-2
- Forgot to update

* Wed Jun 21 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.109-1
- Update to 1.11.109

* Tue May 23 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.90-1
- Update to 1.11.90

* Wed Mar 15 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.63-1
- Update to 1.11.63

* Sat Feb 25 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.55-1
- Update to 1.11.55

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.40-1
- Update to 1.11.40

* Wed Dec 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.34-2
- Update to 1.11.34

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.11.28-3
- Rebuild for Python 3.6

* Tue Dec 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.28-2
- Add PyYAML dependency

* Sun Dec 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.28-1
- Update to 1.11.28

* Sat Dec 03 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.24-1
- Update to 1.11.24

* Thu Nov 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.21-1
- Update to 1.11.21

* Mon Oct 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.12-1
- Update to 1.11.12

* Sun Oct 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.11.0-1
- Update to 1.11.0

* Wed Sep 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.67-1
- Update to 1.10.67

* Wed Sep 07 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.62-1
- Update to 1.10.62

* Wed Aug 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.59-1
- Update to current upstream version

* Fri Aug 05 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.53-1
- Update to current upstream version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.45-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.45-1
- Update to current upstream version

* Wed Jun 08 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.36-1
- Update to current upstream version

* Sat May 28 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.34-1
- Update to current upstream version

* Wed Feb 24 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.7-1
- Update to current upstream version

* Tue Feb 23 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.6-2
- Fix broken dependency

* Fri Feb 19 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.6-1
- Update to current upstream version

* Wed Feb 17 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.5-1
- Update to current upstream version

* Fri Feb 12 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.4-1
- Update to current upstream version

* Wed Feb 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.3-1
- Update to current upstream version

* Tue Feb 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.2-1
- Update to current upstream version

* Tue Feb 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.1-1
- Update to current upstream version

* Fri Jan 22 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.0-1
- Update to current upstream version

* Wed Jan 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.21-1
- Update to current upstream version
- do not fix documentation permissions any more (pull request merged)

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.920-1
- Update to current upstream version

* Fri Jan 15 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.19-1
- Update to current upstream version
- do not substitue the text of bin/aws_bash_completer anymore (pull request merged)
- do not remove the shabang from awscli/paramfile.py anymore (pull request merged)

* Wed Jan 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.18-1
- Update to current upstream version
- Fix completion for bash
- Remove bcdoc dependency that is not used anymore

* Sun Jan 10 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.17-1
- Update to current upstream version
- Lock the botocore dependency version

* Sat Jan 09 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.16-1
- Update to current upstream version
- Add dir /usr/share/zsh
- Add dir /usr/share/zsh/site-functions
- Add MIT license (topictags.py is MIT licensed)
- Move dependency from python-devel to python2-devel
- Add Recommends lines for zsh and bsah-completion for Fedora
- Remove BuildReuires: bash-completion
- Remove the macros py2_build and py2_install to prefer the extended form
- Force non-executable bit for documentation
- Remove shabang from awscli/paramfile.py
- Fix bash completion
- Fix zsh completion
- Remove aws.cmd

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.9.15-1
- Initial package.
