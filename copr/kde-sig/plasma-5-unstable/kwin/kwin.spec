# Whether to build experimental Wayland support
# NOTE: Does not build on F20 due to too old Wayland and requires kf5-kwayland,
# which is not available in Fedora yet
%if 0%{?fedora} > 21
%global  wayland 1
%endif

Name:    kwin
Version: 5.4.90
Release: 1%{?dist}
Summary: KDE Window manager

# all sources are effectively GPLv2+, except for:
# scripts/enforcedeco/contents/code/main.js
# KDE e.V. may determine that future GPL versions are accepted
License: GPLv2 or GPLv3
URL:     https://projects.kde.org/projects/kde/workspace/kwin

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

%global majmin_ver %(echo %{version} | cut -d. -f1,2)

## upstream patches

## upstreamable patches

# Base
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros

# Qt
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtx11extras-devel

# X11/OpenGL
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libXcursor-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  libepoxy-devel

# Wayland (optional)
%if 0%{?wayland}
BuildRequires:  kf5-kwayland-devel >= %{version}
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  libwayland-cursor-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  libxkbcommon-devel >= 0.4
BuildRequires:  pkgconfig(libinput) >= 0.10
BuildRequires:  pkgconfig(libudev)
%endif

# KF5
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kinit-devel >= 5.10.0-3
BuildRequires:  kf5-kio-devel
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
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kiconthemes-devel

BuildRequires:  kdecoration-devel >= %{majmin_ver}
BuildRequires:  kscreenlocker-devel >= %{majmin_ver}

## Runtime deps
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

Requires:       kf5-filesystem
# Runtime-only dependency for effect video playback
Requires:       qt5-qtmultimedia
# libkdeinit5_kwin*
%{?kf5_kinit_requires}

# Before kwin was split out from kde-workspace into a subpackage
Conflicts:      kde-workspace%{?_isa} < 4.11.14-2

Obsoletes:      kwin-gles < 5
Obsoletes:      kwin-gles-libs < 5

# http://bugzilla.redhat.com/605675
Provides: firstboot(windowmanager) = kwin_x11
# and kwin too (#1197135), until initial-setup fixed
Provides: firstboot(windowmanager) = kwin

%description
%{summary}.

%if 0%{?wayland}
%package        wayland
Summary:        KDE Window Manager with experimental Wayland support
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       kwayland-integration%{?_isa} >= %{version}
# libkdeinit5_kwin*
%{?kf5_kinit_requires}
%description    wayland
%{summary}.
%endif

%package        libs
Summary:        KWin runtime libraries
# Before kwin-libs was split out from kde-workspace into a subpackage
Conflicts:      kde-workspace-libs%{?_isa} < 4.11.14-2
%if 0%{?wayland}
# = or >= ? play safe, go with latter for now -- rex
Requires:       kf5-kwayland%{?_isa} >= %{version}
%endif
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
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
%description    doc
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
%find_lang kwin5 --with-qt --with-kde --all-name

# temporary(?) hack to allow initial-setup to use /usr/bin/kwin too
ln -s kwin_x11 %{buildroot}%{_bindir}/kwin


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
%{_bindir}/kwin
%{_bindir}/kwin_x11
%{_kf5_libdir}/libkdeinit5_kwin_x11.so
%{_kf5_libdir}/libkdeinit5_kwin_rules_dialog.so
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
%{_datadir}/icons/hicolor/*/apps/kwin.*
# note: these are for reference (to express config defaults), they are
# not config files themselves (so don't use %%config tag)
%{_sysconfdir}/xdg/*.knsrc

%if 0%{?wayland}
%files wayland
%{_kf5_bindir}/kwin_wayland
%{_kf5_qtplugindir}/platforms/KWinQpaPlugin.so
%{_kf5_qtplugindir}/org.kde.kglobalaccel5.platforms/KF5GlobalAccelPrivateKWin.so
%{_kf5_qtplugindir}/org.kde.kwin.waylandbackends/KWinWaylandDrmBackend.so
%{_kf5_qtplugindir}/org.kde.kwin.waylandbackends/KWinWaylandFbdevBackend.so
%{_kf5_qtplugindir}/org.kde.kwin.waylandbackends/KWinWaylandWaylandBackend.so
%{_kf5_qtplugindir}/org.kde.kwin.waylandbackends/KWinWaylandX11Backend.so
%{_kf5_qtplugindir}/org.kde.kwin.waylandbackends/KWinWaylandVirtualBackend.so
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_sysconfdir}/xdg/org_kde_kwin.categories
%{_libdir}/libkwin.so.*
%{_libdir}/libkwinxrenderutils.so.*
%{_libdir}/libkwineffects.so.*
%{_libdir}/libkwinglutils.so.*
%{_libdir}/libkwin4_effect_builtins.so.*

%files devel
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/cmake/KWinDBusInterface
%{_libdir}/libkwinxrenderutils.so
%{_libdir}/libkwineffects.so
%{_libdir}/libkwinglutils.so
%{_libdir}/libkwin4_effect_builtins.so
%{_includedir}/kwin*.h

%files doc
%doc COMPLIANCE COPYING COPYING.DOC HACKING README
%{_docdir}/HTML/en/kcontrol/


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Sat Oct 24 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- respin (rawhide)

* Fri Oct 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- latest batch of upstream fixes (kde#344278,kde#354164,kde#351763,kde#354090)

* Tue Oct 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-2
- .spec cosmetics, backport kwin/aurorae crasher fix (kde#346857)

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- tigthen kdecorration-devel dep

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- -devel: move dbus xml interface files here

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Wed Sep 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-4
- versioned kf5-kwayland dep too
- make kwayland-integration dep arch'd

* Wed Sep 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- add versioned Requires: kwin-libs dep to main pkg

* Tue Aug 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-2
- add upstream patch to fix crash
- make sure kwayland-integration is installed for kwin-wayland

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- BR: kf5-kcompletion-devel kf5-kiconthemes-devel kf5-kio-devel

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Tue May 19 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-5
- move dbus xml files to -libs (so present for -devel)

* Sun May 17 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.0-4
- followup SM fix, discard support (kde#341930)
- note qt5-qtmultimedia dep is runtime-only

* Thu May 14 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.0-3
- test candidate SM fixes (reviewboard#123580,kde#341930)
- move libkdeinit bits out of -libs
- move dbus interface xml to runtime pkg
- drop %%config from knsrc files
- enable wayland support (f21+)
- .spec cosmetics

* Wed Apr 29 2015 Jan Grulich <jgrulich@redhat.com> - 5.3.0-2
- BR xcb-util-cursor-devel

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Tue Apr 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- tarball respin

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-4
- Rebuild (GCC 5)

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-3
- Provide /usr/bin/kwin too (#1197135)
- bump plasma_version macro

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- Provides: firstboot(windowmanager) = kwin_x11  (#605675)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Sun Feb 08 2015 Daniel Vrátil <dvratli@redhat.com> - 5.2.0.1-2
- Obsoletes: kwin-gles, kwin-gles-libs

* Wed Jan 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0.1-1
- Update to upstream hotfix release 5.2.0.1 (kwindeco KCM bugfix)

* Wed Jan 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-3
- add upstream patch for bug #341971 - fixes Window decorations KCM

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- -doc: Don't require arch-specific kwin in noarch package

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

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
