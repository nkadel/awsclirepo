# Force python38 for RHEL 8, which has python 3.6 by default
%if 0%{?el8} || 0%{?el9}
%global python3_version 3.12
%global python3_pkgversion 3.12
# For RHEL 'platform python' insanity: Simply put, no.
%global __python3 %{_bindir}/python%{python3_version}
%endif

# Created by pyp2rpm-3.3.10
%global pypi_name attr
%global pypi_version 0.3.2

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Simple decorator to set attributes of target function or class in a DRY way

License:        MIT
URL:            https://github.com/denis-ryzhkov/attr
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description
Usage example:: Django proposes: def my_calculated_field(...
my_calculated_field.short_description 'Field'
my_calculated_field.admin_order_field 'real_field' DRY:
@attr(short_description'Field', admin_order_field'real_field') def
my_calculated_field(...Get it:: sudo pip install attr from attr import attrNew
popular attrs.org <>_ used by pytest.org <>_ defines another "attr" package
that...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
Usage example:: Django proposes: def my_calculated_field(...
my_calculated_field.short_description 'Field'
my_calculated_field.admin_order_field 'real_field' DRY:
@attr(short_description'Field', admin_order_field'real_field') def
my_calculated_field(...Get it:: sudo pip install attr from attr import attrNew
popular attrs.org <>_ used by pytest.org <>_ defines another "attr" package
that...


%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/dry_attr.py
#%%{python3_sitelib}/%%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Sun Apr 27 2025 Nico Kadel-Garcia <nkadelg@mail.com> - 0.3.2-1
- Initial package.
