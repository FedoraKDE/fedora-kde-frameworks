Name:           plymouth-theme-breeze
Version:        5.5.95
Release:        1%{?dist}
Summary:        Breeze theme for Plymouth

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/breeze-plymouth-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  plymouth-devel


Requires:       plymouth

%description
%{summary}.

%prep
%autosetup -n breeze-plymouth-%{version} -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_flags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files
%license COPYING
%doc README
%{_libdir}/plymouth/breeze-text.so
%{_datadir}/plymouth/themes/breeze-text/
%{_datadir}/plymouth/themes/breeze/

%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Initial version
