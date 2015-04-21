Name:           plasma-workspace
Version:        5.2.2
Release:        2%{?dist}
Summary:        Plasma workspace, applications and applets
License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/plasma-workspace

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

# This goes to PAM
Source10:       kde
# upstream startkde.kde, minus stuff we don't want or need, plus a minor bit of customization --rex
Source11:       startkde.cmake

## downstream Patches

## upstreamable Patches

## upstream Patches
# http://commits.kde.org/plasma-workspace/24f24e03793c8214a5d1f3414a5aeb48eccef4f4
Patch4: 0004-Workaround-the-lockscreen-password-field-focus-issue.patch

# udev
BuildRequires:  zlib-devel
BuildRequires:  dbusmenu-qt5-devel
BuildRequires:  libGL-devel
BuildRequires:  mesa-libGLES-devel
#BuildRequires:  wayland-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXau-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-devel
BuildRequires:  glib2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  python-devel
BuildRequires:  boost-devel
#BuildRequires:  akonadi-qt5-devel
#BuildRequires:  kdepimlibs-devel
BuildRequires:  libusb-devel
BuildRequires:  libbsd-devel
BuildRequires:  pam-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  pciutils-devel
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
%endif
BuildRequires:  gpsd-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-kjsembed-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-threadweaver-devel
BuildRequires:  kf5-ktexteditor-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdewebkit-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kglobalaccel-devel >= 5.7

BuildRequires:  kf5-ksysguard-devel
BuildRequires:  kf5-kscreen-devel
BuildRequires:  kf5-baloo-devel

BuildRequires:  kf5-kwayland-devel
BuildRequires:  libwayland-client-devel >= 1.3.0
BuildRequires:  libwayland-server-devel >= 1.3.0

BuildRequires:  kwin-devel

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils

# Optional
BuildRequires:  kf5-kactivities-devel


# HACK: Should be kf5-kactivities-runtime, but that conflicts with kactivities,
# so we requre KDE4 KActivities (it's dbus runtime dep, so no problem)
Requires:       kactivities
Requires:       kf5-kinit
Requires:       kf5-kded
Requires:       kf5-kdoctools
#Requires:       kde5-runtime
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtgraphicaleffects
Requires:       kf5-filesystem
Requires:       kf5-baloo
Requires:       kf5-kglobalaccel >= 5.7

# Without the platformtheme plugins we get broken fonts
Requires:       kf5-frameworkintegration

# For krunner
Requires:       plasma-milou

# Power management
Requires:       powerdevil

# startkde
Requires:       coreutils
Requires:       dbus-x11
Requires:       socat
Requires:       xmessage
Requires:       qt5-qttools

Requires:       xorg-x11-utils
Requires:       xorg-x11-server-utils

Requires:       kde-settings

Requires:       systemd

# SysTray support for Qt 4 apps
Requires:       sni-qt

# Oxygen
Requires:       oxygen-icon-theme
Requires:       oxygen-sound-theme
Requires:       oxygen-fonts

# PolicyKit authentication agent
Requires: polkit-kde

%description
Plasma 5 libraries and runtime components


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation and user manuals for %{name}

%description    doc
Documentation and user manuals for %{name}.


%prep
%autosetup -p1

mv startkde/startkde.cmake startkde/startkde.cmake.orig
install -m644 -p %{SOURCE11} startkde/startkde.cmake


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

chrpath --delete %{buildroot}/%{_kf5_qtplugindir}/phonon_platform/kde.so

# Make kcheckpass work
install -m455 -p -D %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/kde
%find_lang plasmaworkspace5 --with-qt --with-kde --all-name


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/{plasma-windowed,org.kde.klipper}.desktop


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f plasmaworkspace5.lang
%{_bindir}/*
%{_libdir}/*.so.*
%{_kf5_libdir}/libkdeinit5_*.so
%{_kf5_qtplugindir}/plasma/dataengine/*.so
%{_kf5_qtplugindir}/plasma/packagestructure/*.so
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/phonon_platform/kde.so
%{_qt5_prefix}/qml/org/kde/*
%{_libexecdir}/*
%{_datadir}/ksmserver
%{_datadir}/ksplash
%{_datadir}/plasma/plasmoids
%{_datadir}/plasma/services
%{_datadir}/plasma/shareprovider
%{_datadir}/plasma/wallpapers
%{_datadir}/plasma/look-and-feel
%{_datadir}/plasma/kcms
%{_datadir}/solid
%{_datadir}/kstyle
%{_datadir}/drkonqi/debuggers/external/*
%{_datadir}/drkonqi/debuggers/internal/*
%{_datadir}/drkonqi/mappings
%{_datadir}/drkonqi/pics/*.png
%{_sysconfdir}/xdg/*.knsrc
%{_sysconfdir}/xdg/taskmanagerrulesrc
%{_sysconfdir}/xdg/autostart/*.desktop
%{_datadir}/desktop-directories/*.directory
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/knotifications5/*.notifyrc
%{_datadir}/applications/*.desktop
%{_datadir}/config.kcfg
%{_datadir}/sddm/themes/breeze
%{_datadir}/xsessions/plasma.desktop

# PAM
%config %{_sysconfdir}/pam.d/kde

%files doc
%{_datadir}/doc/HTML/*/*

%files devel
%{_libdir}/libweather_ion.so
%{_libdir}/libtaskmanager.so
%{_libdir}/libplasma-geolocation-interface.so
%{_libdir}/libkworkspace5.so
%{_includedir}/*
%{_libdir}/cmake/KRunnerAppDBusInterface
%{_libdir}/cmake/KSMServerDBusInterface
%{_libdir}/cmake/LibKWorkspace
%{_libdir}/cmake/LibTaskManager
%{_libdir}/cmake/ScreenSaverDBusInterface

# TODO split to subpackages
# - KCM (?)
# - plasmoids
# - icons
# - individual tools


%changelog
* Wed Mar 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- Lockscreen: Password field does not have focus (kde#344823)

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Mon Mar 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-6
- revert Requires: plasma-desktop (dep should be the other way around)
- drop Obsoletes: kde-workspace (leave for plasma-desktop)
- Requires: polkit-kde

* Sun Mar 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-5
- Requires: -sddm (#1201034), +plasma-desktop

* Fri Mar 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- rebuild (gpsd)

* Tue Mar 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- use our own startkde.cmake

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-8
- (Build)Requires: kf5-kglobalaccel(-devel) >= 5.7
- drop ksyncdbusenv.patch workaround
- .spec cosmetics

* Wed Feb 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-7
- "Could not sync environment to dbus." (startkde) (#1191171)

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-6
- Revert the previous change

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-5
- Provides/Obsoletes: kdeclassic-cursor-theme

* Sun Feb 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-4
- Requires: powerdevil, oxygen-sound-theme

* Thu Jan 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-3
- Requires: plasma-milou (for krunner)

* Thu Jan 29 2015 Dan Horák <dan[at]danny.cz> - 5.2.0-2
- no FireWire on s390(x)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-3.beta
- Requires: kf5-frameworkintegration (provides platformtheme plugin)

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- BR: kf5-kscreen-devel (renamed)

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-5
- Add upstream patch to make ksyncdbusenv work with dbus-1.8.14

* Fri Jan 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-4
- Requires: qt5-qttools (for dbus-qt5)

* Wed Jan 07 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.2-3
- Omit "5" from pkg summary
  Drop config macro for files installed to /etc/xdg
  Move /usr/share/dbus-1/interfaces/*.xml stuff to main package
  Validate .desktop files
  look for qdbus-qt5 in startkde instead of qdbus

* Mon Jan 05 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- add upstream patch to fix black screen on start

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-1
- Plasma 5.1.2

* Fri Nov 28 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-2
- Apply upstream patch to build against new version of KScreen

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Tue Sep 02 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-3
- Make sure we get oxygen-icon-theme and oxyge-icons installed

* Fri Aug 29 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-2
- Add upstream patch to fix generated path in plasma.desktop

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-7
- Add more Obsoletes to make upgrade from KDE 4 smooth
- Add sni-qt to Requires so that Qt 4 apps are working with Plasma 5 systray
- Requires kde-settings

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-4
- Add patch to fix build-time generated paths

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-3
- Use relative BIN_INSTALL_DIR so that built-in paths are correctly generated

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Fix /usr//usr/ in generated files

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Tue May 20 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-6.20140519gita85f5bc
- Add LIBEXEC_PATH to kde5 profile to fix drkonqi lookup
- Fix install 

* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-3.20140519gita85f5bc
- Update to latest git snapshot
- Add PAM file
- Add profile.d entry

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> - 4.95.0-1.20140425git7c97c92
- Initial version of kde5-plasma-workspace
