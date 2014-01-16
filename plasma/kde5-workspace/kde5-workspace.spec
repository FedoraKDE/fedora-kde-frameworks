%define snapshot  20140110

Name:           kde5-workspace
Version:        4.90.1
Release:        4.%{snapshot}git%{?dist}
Summary:        Plasma 2 workspace applications and applets

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/kde-workspace.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}.tar.bz2
Source0:        %{name}-%{version}-%{snapshot}.tar.bz2
Source1:        kde5-plasma.desktop
Source2:        fedora_startkde.sh

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
BuildRequires:  qt5-qtquick1-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  phonon-qt5-devel

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
BuildRequires:  kf5-kprintutils-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kde4support-devel
BuildRequires:  kf5-kdesignerplugin-devel

BuildRequires:  plasma-framework-devel
BuildRequires:  attica-qt5-devel
BuildRequires:  kactivities-qt5-devel


Requires:       kf5-kinit
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
%setup -q -n %{name}-%{version}-%{snapshot}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
# LIBEXEC_INSTALL_DIR automatically prefixed by CMAKE_INSTALL_PREFIX internally
%{cmake_kf5} \
        -DLIBEXEC_INSTALL_DIR=libexec \
        ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# %%{_datadir} here is intended - we need to install to location where DMs look
install -p -m644 -D %{SOURCE1} %{buildroot}/%{_datadir}/xsessions/kde5-plasma.desktop
install -p -m655 -D %{SOURCE2} %{buildroot}/%{_kf5_bindir}/fedora_startkde

# plasma-shell keeps complaining about this ServiceType missing, but it's not
# installeed, because plasmagenericshell is not compiled
install -p -m655 -D %{sourcedir}/libs/plasmagenericshell/plasma-layout-template.desktop \
                    %{buildroot}/%{_kf5_datadir}/kde5/servicetypes/plasma-layout-template.desktop


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

# TODO split to subpackages
# - KCM (?)
# - plasmoids
# - icons
# - individual tools

%files
%{_kf5_bindir}/*
%{_kf5_libdir}/*.so.*
%{_kf5_plugindir}/*.so
%{_kf5_plugindir}/plasma/dataengine/*.so
%{_kf5_plugindir}/plasma/geolocationprovider/*.so
%{_kf5_plugindir}/plasma/packagestructure/*.so
%{_kf5_qtplugindir}/styles/oxygen.so
%{_kf5_qtplugindir}/kf5/*.so
%{_kf5_libdir}/qml/org/kde/*
%{_kf5_libdir}/kconf_update_bin
%{_kf5_libexecdir}/*
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_datadir}/kde5/services/*.protocol
%{_kf5_datadir}/kde5/services/kwin/*.desktop
%{_kf5_datadir}/kde5/services/kded/*.desktop
%{_kf5_datadir}/kde5/services/ServiceMenus/*.desktop
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_datadir}/applications/kde5/*.desktop
%{_kf5_datadir}/systemsettings
%{_kf5_datadir}/config.kcfg
%{_kf5_datadir}/kwin
%{_kf5_datadir}/icons/*
%{_kf5_datadir}/kconf_update/*
%{_kf5_datadir}/ksmserver
%{_kf5_datadir}/ksplash
%{_kf5_datadir}/powerdevil
%{_kf5_datadir}/ksysguard
%{_kf5_datadir}/kcmkeyboard
%{_kf5_datadir}/kcminput
%{_kf5_datadir}/color-schemes
%{_kf5_datadir}/kthememanager
%{_kf5_datadir}/kdisplay
%{_kf5_datadir}/kcontrol
%{_kf5_datadir}/kcmstyle
%{_kf5_datadir}/kcmkeys
%{_kf5_datadir}/kfontinst
%{_kf5_datadir}/kfontview
%{_kf5_datadir}/konqsidebartng
%{_kf5_datadir}/kmenuedit
%{_kf5_datadir}/freespacenotifier
%{_kf5_datadir}/kinfocenter
%{_kf5_datadir}/kcmusb
%{_kf5_datadir}/kcmview1394
%{_kf5_datadir}/khotkeys
%{_kf5_datadir}/kaccess
%{_kf5_datadir}/plasma/plasmoids
%{_kf5_datadir}/plasma/services
%{_kf5_datadir}/plasma/shareprovider
%{_kf5_datadir}/plasma/wallpapers
%{_kf5_datadir}/plasma/shells
%{_kf5_datadir}/plasma/look-and-feel
%{_kf5_datadir}/plasma/packages
%{_kf5_datadir}/solid
%{_kf5_datadir}/kstyle

# %%{_datadir} here is intended - we need to install to location where DMs look
%{_datadir}/xsessions/kde5-plasma.desktop

%{_kf5_sysconfdir}/xdg/*.knsrc
%{_kf5_sysconfdir}/ksysguarddrc
%{_kf5_sysconfdir}/xdg/autostart/*.desktop

%files doc
%doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_kf5_datadir}/doc/HTML/en/*

%files devel
%{_kf5_libdir}/KDE4Workspace/
%{_kf5_libdir}/*.so
%{_kf5_includedir}/*
%{_kf5_datadir}/dbus-1/interfaces/*.xml


%changelog
* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-4
- export KDEHOME in fedora_startkde (otherwise we don't get icons)

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-3
- add some run-time dependencies

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rename to kde5-workspace and bump Release

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- fork kde-workspace to plasma2
