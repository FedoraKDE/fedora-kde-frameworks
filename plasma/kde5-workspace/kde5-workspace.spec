# %define snapshot  20140315

Name:           kde5-workspace
Version:        4.95.0
Release:        1%{?dist}
Summary:        Plasma 2 workspace applications and applets

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/kde-workspace.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/plasma/%{version}/kde-workspace-%{version}.tar.xz
Source0:        kde-workspace-%{version}.tar.xz
Source1:        kde5-plasma.desktop
Source2:        fedora_startkde.sh
Source3:        plasma-shell.desktop

Patch0:         kde-workspace-startkde-fix-kdeinit-lookup.patch
Patch1:         kde-workspace-fix-build.patch

# udev
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  dbusmenu-qt5-devel
BuildRequires:  qimageblitz-devel
BuildRequires:  libGL-devel
BuildRequires:  mesa-libGLES-devel
#BuildRequires:  wayland-devel
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
BuildRequires:  libraw1394-devel
BuildRequires:  gpsd-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtconfiguration-devel
BuildRequires:  qt5-qtquick1-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtwebkit-devel
# FIXME: Why do I need to isntall all backends when depending on QtSql?
BuildRequires:  qt5-qtbase-ibase
BuildRequires:  qt5-qtbase-odbc
BuildRequires:  qt5-qtbase-mysql
BuildRequires:  qt5-qtbase-postgresql
BuildRequires:  qt5-qtbase-tds
BuildRequires:  phonon-qt5-devel

BuildRequires:  kde5-filesystem
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kitemmodels-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-threadweaver-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kjsembed-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kross-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kde4support-devel
BuildRequires:  kf5-kdesignerplugin-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kactivities-libs-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-kemoticons-devel

Requires:       kf5-kinit
Requires:       kf5-kded
Requires:       kf5-kdoctools
Requires:       kde5-runtime
Requires:       qt5-qtquickcontrols

# startkde
Requires:       coreutils
Requires:       dbus-x11

Requires:       xorg-x11-utils
Requires:       xorg-x11-server-utils

# KDM is dead in Plasma 2, so let's use SDDM.
Requires:       sddm

Requires:       systemd


Provides:       plasma2 = %{version}-%{release}
Obsoletes:      plasma2 <= 4.90.1-1.20140110git


%description
Plasma 2 libraries and runtime components


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       plasma2-devel = %{version}-%{release}
Obsoletes:      plasma2-devel <= 4.90.1-1.20140110git

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation and user manuals for %{name}
Provides:       plasma2-doc = %{version}-%{release}
Obsoletes:      plasma2-doc <= 4.90.1-1.20140110git

%description    doc
Documentation and user manuals for %{name}.


%prep
%setup -q -n kde-workspace-%{version}

%patch0 -p1 -b .kde-workspace-startkde-fix-kdeinit-lookup
%patch1 -p1 -b .fix-build.patch

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# %%{_datadir} here is intended - we need to install to location where DMs look
install -p -m644 -D %{SOURCE1} %{buildroot}/%{_datadir}/xsessions/kde5-plasma.desktop
install -p -m655 -D %{SOURCE2} %{buildroot}/%{_kde5_bindir}/fedora_startkde
install -p -m644 -D %{SOURCE3} %{buildroot}/%{_kde5_sysconfdir}/xdg/autostart/plasma-shell.desktop


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kde5_bindir}/*
%{_kde5_libdir}/*.so.*
%{_kde5_plugindir}/kf5/plasma/dataengine/*.so
%{_kde5_plugindir}/kf5/plasma/geolocationprovider/*.so
%{_kde5_plugindir}/kf5/plasma/packagestructure/*.so
%{_kde5_plugindir}/styles/oxygen.so
%{_kde5_plugindir}/kf5/*.so
%{_kde5_libdir}/qml/org/kde/*
%{_kde5_libdir}/kconf_update_bin
%{_kde5_libdir}/cmake/KF5SysGuard
%{_kde5_libdir}/cmake/KHotKeysDBusInterface
%{_kde5_libdir}/cmake/KRunnerAppDBusInterface
%{_kde5_libdir}/cmake/KSMServerDBusInterface/*.cmake
%{_kde5_libdir}/cmake/KWinDBusInterface/*.cmake
%{_kde5_libdir}/cmake/LibKWorkspace/*.cmake
%{_kde5_libdir}/cmake/LibTaskManager/*.cmake
%{_kde5_libexecdir}/*
%{_kde5_datadir}/kde5/services/*.desktop
%{_kde5_datadir}/kde5/services/*.protocol
%{_kde5_datadir}/kde5/services/kwin/*.desktop
%{_kde5_datadir}/kde5/services/kded/*.desktop
%{_kde5_datadir}/kde5/services/ServiceMenus/*.desktop
%{_kde5_datadir}/kde5/servicetypes/*.desktop
%{_kde5_datadir}/applications/*.desktop
%{_kde5_datadir}/systemsettings
%{_kde5_datadir}/config.kcfg
%{_kde5_datadir}/kwin
%{_kde5_datadir}/icons/*
%{_kde5_datadir}/kconf_update/*
%{_kde5_datadir}/ksmserver
%{_kde5_datadir}/ksplash
%{_kde5_datadir}/powerdevil
%{_kde5_datadir}/ksysguard
%{_kde5_datadir}/kcmkeyboard
%{_kde5_datadir}/kcminput
%{_kde5_datadir}/color-schemes
%{_kde5_datadir}/kthememanager
%{_kde5_datadir}/kdisplay
%{_kde5_datadir}/kcontrol
%{_kde5_datadir}/kcmstyle
%{_kde5_datadir}/kcmkeys
%{_kde5_datadir}/kfontinst
%{_kde5_datadir}/kfontview
%{_kde5_datadir}/konqsidebartng
%{_kde5_datadir}/kmenuedit
%{_kde5_datadir}/freespacenotifier
%{_kde5_datadir}/kinfocenter
%{_kde5_datadir}/kcmusb
%{_kde5_datadir}/kcmview1394
%{_kde5_datadir}/khotkeys
%{_kde5_datadir}/kaccess
%{_kde5_datadir}/kwrited
%{_kde5_datadir}/plasma/plasmoids
%{_kde5_datadir}/plasma/services
%{_kde5_datadir}/plasma/shareprovider
%{_kde5_datadir}/plasma/wallpapers
%{_kde5_datadir}/plasma/shells
%{_kde5_datadir}/plasma/look-and-feel
%{_kde5_datadir}/plasma/packages
%{_kde5_datadir}/solid
%{_kde5_datadir}/kstyle
%{_kde5_datadir}/sounds/pop.wav
# %%{_datadir} here is intended - we need to install to location where DMs look
%{_datadir}/xsessions/kde5-plasma.desktop

%{_kde5_plugindir}/kf5/kwin


%{_kde5_sysconfdir}/xdg/*.knsrc
%{_kde5_sysconfdir}/ksysguarddrc
%{_kde5_sysconfdir}/xdg/autostart/*.desktop

%files doc
# %doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_kde5_datadir}/doc/HTML/en/*

%files devel
%{_kde5_libdir}/*.so
%{_kde5_libdir}/cmake/KDecorations/
%{_kde5_includedir}/*
%{_kde5_datadir}/dbus-1/interfaces/*.xml
%{_kde5_datadir}/dbus-1/services/org.kde.krunner.service

# TODO split to subpackages
# - KCM (?)
# - plasmoids
# - icons
# - individual tools


%changelog
* Wed Apr 02 2014 Jan Grulich <jgrulich@redhat.com> 4.95.0-1
- Update to Alpha 1

* Mon Mar 24 2014 Jan Grulich <jgrulich@redhat.com 4.90.1-7.20140315git
- fix plasma-shell autostart

* Sat Mar 15 2014 Jan Grulich <jgrulich@redhat.com 4.90.1-6.20140315git
- update git snapshot

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-5.20140213git
- update to latest git snapshot

* Sat Feb 08 2014 Martin Briza <mbriza@redhat.com> 4.95.0-6
- prevent annoying errors on package removing

* Tue Jan 21 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-5
- fix installation of a ,desktop file
- add kf5-kded to runtime deps

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-4
- export KDEHOME in fedora_startkde (otherwise we don't get icons)

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-3
- add some run-time dependencies

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rename to kde5-workspace and bump Release

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- fork kde-workspace to plasma2
