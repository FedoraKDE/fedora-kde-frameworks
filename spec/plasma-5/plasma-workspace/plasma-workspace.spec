Name:           plasma-workspace
Version:        5.0.0
Release:        1%{?dist}
Summary:        Plasma 5 workspace applications and applets
License:        GPLv2+
URL:            http://www.kde.org

Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

# This goes to PAM
Source10:       kde

# udev
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
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdewebkit-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-ksysguard-devel
BuildRequires:  kf5-kscreen-devel
BuildRequires:  kf5-baloo-devel

BuildRequires:  kwin-devel

# FIXME: Missing kf5-kdepimlibs-umbrella

BuildRequires:  chrpath

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
Requires:       kf5-filesystem
Requires:       kf5-baloo

# startkde
Requires:       coreutils
Requires:       dbus-x11
Requires:       socat
Requires:       xmessage

Requires:       xorg-x11-utils
Requires:       xorg-x11-server-utils

# KDM is dead in Plasma 5, so let's use SDDM.
Requires:       sddm

Requires:       systemd

Obsoletes:      kde-workspace < 5.0.0-1

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
%setup -q

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

chrpath --delete %{buildroot}/%{_kf5_qtplugindir}/phonon_platform/kde.so

# Makes kcheckpass work
install -m455 -p -D %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/kde
%find_lang plasmaworkspace5 --with-qt --all-name

# Fix startkde being stupid and broken
#sed -i 's/lib\(\|64\)\/kde5\/libexec/libexec/' %{buildroot}/%{_kde5_bindir}/startkde

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f plasmaworkspace5.lang
%{_bindir}/*
%{_libdir}/*.so.*
%{_kf5_libdir}/libkdeinit5_*.so
%{_libdir}/libKF5XmlRpcClientPrivate.so
%{_kf5_qtplugindir}/plasma/dataengine/*.so
%{_kf5_qtplugindir}/plasma/geolocationprovider/*.so
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
%{_datadir}/solid
%{_datadir}/kstyle
%{_datadir}/drkonqi/debuggers/external/*
%{_datadir}/drkonqi/debuggers/internal/*
%{_datadir}/drkonqi/mappings
%{_datadir}/drkonqi/pics/*.png
%config %{_sysconfdir}/xdg/*.knsrc
%config %{_sysconfdir}/xdg/autostart/*.desktop
%{_datadir}/desktop-directories/*.directory
%{_datadir}/dbus-1/services/*.service
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
# %doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_datadir}/doc/HTML/en/*

%files devel
%{_libdir}/libweather_ion.so
%{_libdir}/libtaskmanager.so
%{_libdir}/libkworkspace.so
%{_libdir}/libplasma-geolocation-interface.so
%{_includedir}/*
%{_libdir}/cmake/KRunnerAppDBusInterface
%{_libdir}/cmake/KSMServerDBusInterface
%{_libdir}/cmake/LibKWorkspace
%{_libdir}/cmake/LibTaskManager
%{_libdir}/cmake/ScreenSaverDBusInterface
%{_datadir}/dbus-1/interfaces/*.xml

# TODO split to subpackages
# - KCM (?)
# - plasmoids
# - icons
# - individual tools


%changelog
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
