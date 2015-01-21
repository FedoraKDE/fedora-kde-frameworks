# Whether to build experimental Wayland support
# NOTE: Does not build on F20 due to too old Wayland and requires kf5-kwayland,
# which is not available in Fedora yet
%global         wayland 0

Name:           kwin
Version:        5.1.95
Release:        1.beta%{?dist}
Summary:        KDE Window manager

# all sources are effectively GPLv2+, except for:
# scripts/enforcedeco/contents/code/main.js
# KDE e.V. may determine that future GPL versions are accepted
License:        GPLv2 or GPLv3
URL:            https://projects.kde.org/projects/kde/workspace/kwin

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

# Base
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

# Qt
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtmultimedia-devel

# X11/OpenGL
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libXcursor-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libepoxy-devel

# Wayland (optional)
%if 0%{?wayland}
BuildRequires:  kf5-kwayland-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  libwayland-cursor-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  libxkbcommon-devel >= 0.4
%endif

# KF5
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kactivities-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  kdecoration-devel

# Runtime deps
Requires:       kf5-filesystem
Requires:       qt5-qtmultimedia

# Before kwin was split out from kde-workspace into a subpackage
Conflicts:      kde-workspace%{?_isa} < 4.11.14-2

%description
%{summary}.

%if 0%{wayland}
%package        wayland
Summary:        KDE Window Manager with experimental Wayland support
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description    wayland
%{summary}.
%endif

%package        libs
Summary:        KWin runtime libraries
# Before kwin-libs was split out from kde-workspace into a subpackage
Conflicts:      kde-workspace-libs%{?_isa} < 4.11.14-2
%description    libs
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-devel
Requires:       kf5-kservice-devel
Requires:       kf5-kwindowsystem-devel
Conflicts:      kde-workspace-devel < 5.0.0-1
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        User manual for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch
%description    doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kwin5 --with-qt --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f kwin5.lang
%{_bindir}/kwin_x11
%{_datadir}/kwin
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/kwin
%{_kf5_qtplugindir}/org.kde.kdecoration2/*.so
%{_qt5_prefix}/qml/org/kde/kwin
%{_kf5_libdir}/kconf_update_bin/kwin5_update_default_rules
%{_libexecdir}/kwin_killer_helper
%{_libexecdir}/kwin_rules_dialog
%{_datadir}/kwincompositing
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kwin
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/knotifications5/kwin.notifyrc
%{_kf5_datadir}/config.kcfg/kwin.kcfg
%{_datadir}/icons/hicolor/*/apps/*
%config %{_sysconfdir}/xdg/*.knsrc

%if 0%{wayland}
%files wayland
%{_bindir}/kwin_wayland
%endif


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libkdeinit5_kwin_x11.so
%if 0%{wayland}
%{_kf5_libdir}/libkdeinit5_kwin_wayland.so
%endif
%{_kf5_libdir}/libkdeinit5_kwin_rules_dialog.so
%{_libdir}/libkwin.so.*
%{_libdir}/libkwinxrenderutils.so.*
%{_libdir}/libkwineffects.so.*
%{_libdir}/libkwinglutils.so.*
%{_libdir}/libkwin4_effect_builtins.so.*

%files devel
%{_libdir}/cmake/KWinDBusInterface
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/libkwinxrenderutils.so
%{_libdir}/libkwineffects.so
%{_libdir}/libkwinglutils.so
%{_libdir}/libkwin4_effect_builtins.so
%{_includedir}/*.h

%files doc
%doc COMPLIANCE COPYING COPYING.DOC HACKING README
%{_datadir}/doc/HTML/en/kcontrol/*


%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Tue Nov 18 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-3
- Fixed license
- Fixed scriptlets
- Fixed Conflicts in -devel
- -docs is noarch

* Wed Nov 12 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-2
- added optional Wayland support

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1.20140514git61c631c
- Update to latest upstream git snapshot

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1.20140425gitb92f4a6
- Initial package
