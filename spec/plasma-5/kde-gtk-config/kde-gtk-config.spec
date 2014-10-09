Name:           kde-gtk-config
Version:        5.1.0
Release:        1%{?dist}
Summary:        Configure the appearance of GTK apps in KDE

License:        GPLv2+
URL:            http://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

%if 0
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcmutils-devel
%endif

Requires:       kf5-filesystem

%description
%{summary}.

%prep
%setup -q

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LIB README
%config %{_sysconfdir}/xdg/*.knsrc
%{_kf5_qtplugindir}/kcm_kdegtkconfig.so
%{_libexecdir}/gtk3_preview
%{_libexecdir}/gtk_preview
%{_libexecdir}/reload_gtk_apps
%{_datadir}/icons/hicolor/*/apps/kde-gtk-config.*
%{_datadir}/kcm-gtk-module
%{_kf5_datadir}/kservices5/kde-gtk-config.desktop


%changelog
* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0
