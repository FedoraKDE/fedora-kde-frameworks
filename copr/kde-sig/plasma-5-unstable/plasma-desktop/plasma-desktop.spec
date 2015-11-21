
%global kf5_version 5.13.0

Name:    plasma-desktop
Summary: Plasma Desktop shell
Version: 5.4.90
Release: 1%{?dist}

License: GPLv2+ and (GPLv2 or GPLv3)
URL:     https://projects.kde.org/projects/kde/workspace/plasma-desktop

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

%global majmin_ver %(echo %{version} | cut -d. -f1,2)

## downstream patches
# default kickoff favorites: -preferred_browser(buggy) +firefox +konsole +apper
Patch100: plasma-desktop-5.4.0-default_favorites.patch
# default kickoff favorites: -preferred_browser(buggy) +konqbrowser +konsole +apper
Patch101: plasma-desktop-5.4.0-default_favorites_f22.patch
# Default to Folder containment (rather than Desktop)
Patch102: plasma-desktop-fedora_layout.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1250238
# http://bugs.kde.org/show_bug.cgi?id=348678
Patch103: plasma-desktop-C_locale.patch

## upstream patches

## upstreamable patches

BuildRequires:  libusb-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libX11-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pkgconfig(xkeyboard-config)

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  phonon-qt5-devel

# PackageKit-Qt 5 is not avaialble on F20, because PackageKit is too old there
%if 0%{?fedora} >= 21
BuildRequires:  PackageKit-Qt5-devel
Recommends: muon-discover
%endif

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-plasma-devel >= %{kf5_version}
BuildRequires:  kf5-kdoctools-devel >= %{kf5_version}
BuildRequires:  kf5-ki18n-devel >= %{kf5_version}
BuildRequires:  kf5-kcmutils-devel >= %{kf5_version}
BuildRequires:  kf5-kglobalaccel-devel >= %{kf5_version}
BuildRequires:  kf5-knewstuff-devel >= %{kf5_version}
BuildRequires:  kf5-kdelibs4support-devel >= %{kf5_version}
BuildRequires:  kf5-knotifyconfig-devel >= %{kf5_version}
BuildRequires:  kf5-kdesu-devel >= %{kf5_version}
BuildRequires:  kf5-attica-devel >= %{kf5_version}
BuildRequires:  kf5-kwallet-devel >= %{kf5_version}
BuildRequires:  kf5-krunner-devel >= %{kf5_version}
BuildRequires:  kf5-baloo-devel >= %{kf5_version}
BuildRequires:  kf5-kdeclarative-devel >= %{kf5_version}
BuildRequires:  kf5-kpeople-devel >= %{kf5_version}
BuildRequires:  kf5-kded-devel >= %{kf5_version}
BuildRequires:  kf5-kinit-devel >= %{kf5_version}
# libkdeinit5_*
%{?kf5_kinit_requires}

BuildRequires:  kf5-ksysguard-devel >= %{majmin_ver}

BuildRequires:  kscreenlocker-devel >= %{majmin_ver}
BuildRequires:  plasma-workspace-devel >= %{majmin_ver}
BuildRequires:  kwin-devel >= %{majmin_ver}

# Optional
BuildRequires:  kf5-kactivities-devel >= %{kf5_version}
BuildRequires:  libcanberra-devel
BuildRequires:  boost-devel
BuildRequires:  pulseaudio-libs-devel

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils

# for kcm_touchpad
BuildRequires:  xorg-x11-drv-synaptics-devel
# for xserver-properties
BuildRequires:  xorg-x11-server-devel
Requires:       kf5-kded

# for kcm_keyboard
Requires:       iso-codes

# for kcm_input
%if 0%{?fedora} > 20
BuildRequires:  xorg-x11-drv-evdev-devel
%endif

# Desktop
Requires:       plasma-workspace >= %{majmin_ver}
Requires:       kf5-filesystem >= %{kf5_version}

# Install breeze
Requires:       plasma-breeze >= %{majmin_ver}
Requires:       breeze-icon-theme >= %{majmin_ver}
Requires:       kde-style-breeze >= %{majmin_ver}

# Install systemsettings, full set of KIO slaves and write() notifications
Requires:       plasma-systemsettings >= %{majmin_ver}
Requires:       kio-extras
Requires:       kwrited >= %{majmin_ver}

# Install KWin
Requires:       kwin >= %{majmin_ver}

# kickoff -> edit applications (#1229393)
Requires:       kmenuedit >= %{majmin_ver}

# kickoff -> uninstall feature
Recommends:     muon-discover >= %{majmin_ver}

# KCM touchpad has been merged to plasma-desktop in 5.3
Provides:       kcm_touchpad = %{version}-%{release}
Obsoletes:      kcm_touchpad < 5.3.0

# Virtual provides for plasma-workspace
Provides:       plasmashell(desktop) = %{version}-%{release}
Provides:       plasmashell = %{version}-%{release}

Obsoletes:      kde-workspace < 5.0.0-1

%description
%{summary}.

%package        doc
Summary:        Documentation and user manuals for %{name}
# per https://bugzilla.redhat.com/show_bug.cgi?id=1199720
# I abhor unversioned Obsoletes, so adding one here with Epoch:1 to be on the safe side -- rex
Obsoletes:      kde-runtime-docs < 1:14.12.3-2
# when conflicting HTML docs were removed
Conflicts:      kcm_colors < 1:4.11.16-10
# when made noarch
Obsoletes: plasma-desktop-doc < 5.3.1-2
BuildArch: noarch
%description    doc
%{summary}.


%prep
%setup -q

%if 0%{?fedora} > 22
%patch100 -p1 -b .default_favorites
%else
%patch101 -p1 -b .default_favorites_f22
%endif
%patch102 -p1 -b .fedora_layout
%if 0%{?fedora} < 24
%patch103 -p1 -b .C_locale
%endif


%build

mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang plasmadesktop5 --with-qt --all-name

# No -devel
rm -fv %{buildroot}%{_libdir}/libkfontinst{,ui}.so

# Copy konqsidebartng to kde4/apps so that KDE Konqueror can find it
mkdir -p %{buildroot}%{_datadir}/kde4/apps/konqsidebartng/virtual_folders/services/
cp %{buildroot}%{_datadir}/konqsidebartng/virtual_folders/services/fonts.desktop \
   %{buildroot}%{_datadir}/kde4/apps/konqsidebartng/virtual_folders/services

# create own `kf5-config --path data`/plasma/shells/org.kde.plasma.desktop/updates/
# per https://techbase.kde.org/KDE_System_Administration/PlasmaTwoDesktopScripting#Running_Scripts
mkdir -p %{buildroot}{_datadir}/plasma/shells/org.kde.plasma.desktop/updates/

## unpackaged files
rm -rfv %{buildroot}%{_datadir}/kdm/pics/users/


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/org.kde.{kfontview,knetattach}.desktop


%post
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files -f plasmadesktop5.lang
%license COPYING*
%if 0%{?fedora} > 20
%{_bindir}/kapplymousetheme
%endif
%{_bindir}/kaccess
%{_bindir}/kfontinst
%{_bindir}/kfontview
%{_bindir}/krdb
%{_bindir}/knetattach
%{_bindir}/solid-action-desktop-gen
%{_kf5_libexecdir}/kauth/kcmdatetimehelper
%{_kf5_libexecdir}/kauth/fontinst
%{_kf5_libexecdir}/kauth/fontinst_helper
%{_kf5_libexecdir}/kauth/fontinst_x11
%{_libexecdir}/kfontprint
%{_qt5_prefix}/qml/org/kde/plasma/private
%{_kf5_libdir}/libkdeinit5_kaccess.so
%{_kf5_libdir}/kconf_update_bin/*
# TODO: -libs subpkg -- rex
%{_kf5_libdir}/libkfontinst.so.*
%{_kf5_libdir}/libkfontinstui.so.*
%{_kf5_libdir}/libKF5ActivitiesExperimentalStats.so.*
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/kcms/*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_qmldir}/org/kde/plasma/activityswitcher
%{_kf5_qmldir}/org/kde/private/desktopcontainment/*
%{_kf5_datadir}/plasma/*
%if 0%{?fedora} > 20
%{_kf5_datadir}/kcminput
%endif
%{_kf5_datadir}/color-schemes
%{_kf5_datadir}/kconf_update/*
%{_kf5_datadir}/kdisplay
%{_kf5_datadir}/kcontrol
%{_kf5_datadir}/kcmkeys
%{_kf5_datadir}/kcm_componentchooser
%{_kf5_datadir}/kcm_phonon
%{_kf5_datadir}/kfontinst
%{_kf5_datadir}/kcmkeyboard
%{_kf5_datadir}/ksmserver
%{_kf5_datadir}/kpackage/kcms/*
%{_datadir}/konqsidebartng/virtual_folders/services/fonts.desktop
%{_datadir}/kde4/apps/konqsidebartng/virtual_folders/services/fonts.desktop
%{_kf5_datadir}/kcmsolidactions
%{_kf5_datadir}/solid/devices/*.desktop
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%config %{_sysconfdir}/xdg/*.knsrc
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/ServiceMenus/installfont.desktop
%{_kf5_datadir}/kservices5/fonts.protocol
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/kxmlgui5/kfontview
%{_kf5_datadir}/kxmlgui5/kfontinst
%{_kf5_datadir}/knotifications5/*.notifyrc
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/org.kde.fontinst.policy
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmclock.policy
# kcm_touchpad
%{_bindir}/kcm-touchpad-list-devices
%{_kf5_qtplugindir}/plasma/dataengine/plasma_engine_touchpad.so
%{_datadir}/config.kcfg/touchpad.kcfg
%{_datadir}/config.kcfg/touchpaddaemon.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.touchpad.xml

%files doc
%lang(ca) %{_docdir}/HTML/ca/kcontrol/
%lang(ca) %{_docdir}/HTML/ca/kfontview/
%lang(ca) %{_docdir}/HTML/ca/knetattach/
%lang(ca) %{_docdir}/HTML/ca/plasma-desktop/
%lang(en) %{_docdir}/HTML/en/kcontrol/
%lang(en) %{_docdir}/HTML/en/kfontview/
%lang(en) %{_docdir}/HTML/en/knetattach/
%lang(en) %{_docdir}/HTML/en/plasma-desktop/
%lang(it) %{_docdir}/HTML/it/plasma-desktop/
%lang(nl) %{_docdir}/HTML/nl/plasma-desktop/
%lang(pt_BR) %{_docdir}/HTML/pt_BR/plasma-desktop/
%lang(ru) %{_docdir}/HTML/ru/plasma-desktop/
%lang(sv) %{_docdir}/HTML/sv/plasma-desktop/
%lang(uk) %{_docdir}/HTML/uk/plasma-desktop/


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-5
- Recommends: muon-discover (#1224421)

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- revert default_favorites.patch back to apper

* Fri Oct 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- default_favorites.patch: -apper, +muon-discover

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-2
- Recommends: muon-discover
- consistently use %%{majmin_ver} macro for plasma5-related dependencies

* Fri Oct 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2, use %%license, .spec cosmetics

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-7
- relax some deps %%{version} => %%{majmin_ver} to ease bootstrapping

* Mon Sep 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-6
- re-fix font management, kauth_helper paths (#1208229, kde#353215)

* Mon Sep 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- restore f22 default favorites

* Fri Sep 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- conditionally apply C.UTF-8 workaround only for < f24 (#1250238)

* Sat Sep 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- tighten build deps (simimlar to plasma-workspace)

* Fri Sep 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- make kio-extras unversioned (it's in kde-apps releases now)

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-4
- Wrong C.UTF-8 locale (#1250238)

* Fri Sep 04 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- make plasma-related runtime deps versioned

* Tue Sep 01 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-2
- Try rebuild against new Baloo

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 5.3.2-5
- rebuild for Boost 1.58

* Tue Jul 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-4
- BR: pkgconfig(xkeyboard-config)

* Mon Jul 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-3
- Switch to Next Keyboard Layout shortcut restores after OS restarting (#1234082)

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- pull in upstream fix for kcm_touchpad: No touchpad found (#1199825)

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Tue Jun 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-7
- kcm_touchpad: No touchpad found (#1199825)

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-6
- kcm_phonon does not display all HDMI audio ports (#1232903)

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-5
- backport trashcan applet fix (#1231972,kde#349207)

* Mon Jun 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- backport "Fix-dropping-files-onto-the-desktop-containment"
- BR: kf5-kglobalaccel-devel

* Mon Jun 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- Requires: kmenuedit, instead of Recommends which doesn't seem to work reliably yet (#1229393)

* Tue Jun 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.1-2
- use %%{kf5_kinit_requires}
- -doc: noarch, %%lang'ify
- Provides: plasmashell

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Thu May 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-6
- default to folder containment (#1220862)

* Fri May 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-5
- Recommends: kmenuedit

* Sun May 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-4
- (re)fix fontinst service paths (#1208229)

* Wed Apr 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-3
- Provides plasmashell(desktop) (#1215691)

* Tue Apr 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Provides/Obsoletes kcm_touchpad (#1216897)

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Thu Apr 23 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Thu Apr 23 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.2-5
- fix fontinst service paths harder (#1208229)
- Konqueror "favorite" opens as a file manager (#1209169)

* Thu Apr 02 2015 Daniel Vrátil <dvratil@redhat.com> 5.2.2-4
- fix fontinst service paths (rhbz#1208229)

* Mon Mar 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-3
- own /usr/share/plasma/shells/org.kde.plasma.desktop/updates

* Fri Mar 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- -doc: Conflicts: kcm_colors < 1:4.11.16-10 (drop conflicts in main pkg)

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Wed Mar 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-6
- adjust default kickoff favorites: +konsole +apper

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-5
- .spec cleanup
- pull in upstream fixes, particularly...
- Top level "tabs" disappears in Kickoff (kde#343524)

* Sat Mar 07 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-4
- -doc: Obsoletes: kde-runtime-docs (#1199720)
- %%find_lang: drop --with-kde, we want handbooks in -doc instead

* Fri Mar 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-3
- Does not obsolete kcm_colors anymore (KDE 4 version is co-installable now)

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-5
- Requires: iso-codes (for kcm_keyboard)

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-4
- Copy konqsidebartng to /usr/share/kde4/apps so that KDE4 Konqueror can find it

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-3
- Workaround broken DBus service file generated by CMake

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Requires: breeze, systemsettings, kwin (for full Plasma experience)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- Obsoletes/Provides kcm_colors

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Jan 07 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.2-3
- Omit "5" from pkg summary
  Add icon cache scriptlets
  Validate application .desktop files
  Fixed license

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

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

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git532fc47
- Initial version of kde5-plasma-desktop
