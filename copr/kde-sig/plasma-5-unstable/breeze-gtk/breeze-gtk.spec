Name:           breeze-gtk
Version:        5.4.90
Release:        1%{?dist}
Summary:	Breeze widget theme for Gtk2 and Gtk3

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

Requires:       kf5-filesystem
# Obviously :)
Requires:       gtk2

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%license COPYING.LIB
%doc README.md
%{_datadir}/themes/Breeze
%{_datadir}/themes/Breeze-Dark
%{_kf5_libdir}/kconf_update_bin/gtkbreeze5.5
%{_kf5_datadir}/kconf_update/gtkbreeze5.5.upd

%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90
