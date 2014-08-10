%define base_name   breeze

Name:           plasma-breeze
Version:        5.0.1
Release:        1%{?dist}
Summary:        Artwork, styles and assets for the Breeze visual style for the Plasma Desktop

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{base_name}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

Requires:       kf5-filesystem

%description
%{summary}.

%prep
%setup -q -n %{base_name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%files
%doc cursors/src/README COPYING
%{_datadir}/color-schemes/Breeze.colors
%{_datadir}/icons/breeze_cursors
%{_datadir}/icons/breeze
%{_datadir}/kwin/decorations/kwin4_decoration_qml_breeze
%{_kf5_datadir}/kservices5/kwin/kwin4_decoration_qml_breeze.desktop
%{_qt5_prefix}/qml/QtQuick/Controls/Styles/Breeze
%{_datadir}/QtCurve/Breeze.qtcurve
%{_kf5_libdir}/kconf_update_bin/kde4breeze
%{_kf5_datadir}/kconf_update/kde4breeze.upd
%{_datadir}/wallpapers/Next

%changelog
* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git73a19ea
- Update to latest upstream

* Fri May 02 2014 Jan Grulich <jgrulich@redhat.com> 4.90.1-0.1.20140502git
- Initial version
