# %define snapshot  20140315
%define git_commit a85f5bc
%define base_name plasma-workspace

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        4.20140519git%{git_commit}%{?dist}
Summary:        Plasma 2 workspace applications and applets

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/kde-workspace.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/plasma/%{version}/kde-workspace-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

# This goes to PAM
Source10:       kde

Patch0:         plasma-workspace-fix-build.patch
Patch1:         plasma-workspace-fix-build-2.patch

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

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
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

BuildRequires:  kde5-kwin-devel

# FIXME: Missing kf5-kdepimlibs-umbrella

BuildRequires:  chrpath

BuildRequires:  kde5-kwin

# Optional
BuildRequires:  kf5-kactivities-libs-devel

# HACK: Should be kf5-kactivities-runtime, but that conflicts with kactivities,
# so we requre KDE4 KActivities (it's dbus runtime dep, so no problem)
Requires:       kactivities
Requires:       kf5-kinit
Requires:       kf5-kded
Requires:       kf5-kdoctools
#Requires:       kde5-runtime
Requires:       qt5-qtquickcontrols
Requires:       kde5-filesystem

# startkde
Requires:       coreutils
Requires:       dbus-x11
Requires:       socat
Requires:       xmessage

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
%setup -q -n %{base_name}-%{version}

%patch0 -R -p1 -b .fixbuild
%patch1 -R -p1 -b .fixbuild2

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} .. \
        -DINCLUDE_INSTALL_DIR:PATH=/usr/include
# FIXME: Remove ^^ once fixed upstream
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

mkdir -p %{buildroot}/%{_datadir}/xsessions
cat <<EOF >> %{buildroot}/%{_datadir}/xsessions/kde5-plasma.desktop
[Desktop Entry]
Encoding=UTF-8
Type=XSession
Exec=%{_kde5_bindir}/startkde
TryExec=%{_kde5_bindir}/startkde
Name=Plasma 2
Comment=The next generation desktop made by the KDE Community
EOF

#mkdir -p %{buildroot}/%{_kde5_bindir}
#cat <<EOF >> %{buildroot}/%{_kde5_bindir}/fedora_startkde
#%{_kde5_bindir}/startkde
#EOF
#chmod a+x %{buildroot}/%{_kde5_bindir}/fedora_startkde

mkdir -p %{buildroot}/%{_kde5_sysconfdir}/profile.d
cat > %{buildroot}/%{_kde5_sysconfdir}/profile.d/kde5.sh << EOF
export XDG_DATA_DIRS="/usr/share/kf5:/usr/share/kde5:/usr/share"
export QT_PLUGIN_PATH="/usr/lib64/kde5/plugins:/usr/lib64/qt5/plugins/kf5:/usr/lib64/qt5/plugins"
export QML2_IMPORT_PATH="/usr/lib64/qt5/qml:/usr/lib64/kde5/qml"
export LD_LIBRARY_PATH="/usr/lib64/kde5:/usr/lib64"
export XDG_ICON_DIRS="/usr/share/icons"
export LIBEXEC_PATH="/usr/libexec/kde5:/usr/libexec/kf5:/usr/libexec"
EOF


mkdir -p %{buildroot}/%{_kde5_plugindir}/phonon_platform
mv %{buildroot}/%{_kde5_plugindir}/{plugins,}/phonon_platform/kde.so
chrpath --delete %{buildroot}/%{_kde5_plugindir}/phonon_platform/kde.so

# These two are ignoring CMAKECONFIG_INSTALL_PREFIX
mv %{buildroot}/%{_kde5_libdir}/cmake/LibKWorkspace %{buildroot}/%{_libdir}/cmake
mv %{buildroot}/%{_kde5_libdir}/cmake/LibTaskManager %{buildroot}/%{_libdir}/cmake

# Makes kcheckpass work
install -m455 -p -D %{SOURCE10} %{buildroot}%{_kde5_sysconfdir}/pam.d/kde

# Fix startkde being stupid and broken
sed -i 's/lib\(\|64\)\/kde5\/libexec/libexec/' %{buildroot}/%{_kde5_bindir}/startkde


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kde5_bindir}/*
%{_kde5_libdir}/*.so.*
%{_kde5_plugindir}/plasma/dataengine/*.so
%{_kde5_plugindir}/plasma/geolocationprovider/*.so
%{_kde5_plugindir}/plasma/packagestructure/*.so
%{_kde5_plugindir}/*.so
%{_kde5_plugindir}/phonon_platform/kde.so
%{_kde5_libdir}/qml/org/kde/*
%{_kde5_libexecdir}/*
%{_kde5_datadir}/ksmserver
%{_kde5_datadir}/ksplash
%{_kde5_datadir}/plasma/plasmoids
%{_kde5_datadir}/plasma/services
%{_kde5_datadir}/plasma/shareprovider
%{_kde5_datadir}/plasma/wallpapers
%{_kde5_datadir}/plasma/look-and-feel
%{_kde5_datadir}/solid
%{_kde5_datadir}/kstyle
%{_kde5_datadir}/drkonqi/debuggers/external/*
%{_kde5_datadir}/drkonqi/debuggers/internal/*
%{_kde5_datadir}/drkonqi/mappings
%{_kde5_datadir}/drkonqi/pics/*.png
%{_kde5_sysconfdir}/xdg/*.knsrc
%{_kde5_sysconfdir}/xdg/autostart/*.desktop
%{_datadir}/desktop-directories/*.directory
%{_datadir}/dbus-1/services/*.service
%{_datadir}/kservices5/*.desktop
%{_datadir}/kservices5/*.protocol
%{_datadir}/kservices5/kded/*.desktop
%{_datadir}/kservicetypes5/*.desktop
%{_datadir}/knotifications5/*.notifyrc
%{_datadir}/applications/*.desktop
%{_datadir}/config.kcfg


%{_datadir}/xsessions/kde5-plasma.desktop

# PAM
%{_kde5_sysconfdir}/pam.d/kde

# Profile.d
%{_kde5_sysconfdir}/profile.d/kde5.sh

%files doc
# %doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_datadir}/doc/HTML/en/*

%files devel
%{_kde5_libdir}/*.so
%{_kde5_includedir}/*
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
* Tue May 20 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-4.20140519gita85f5bc
- Add LIBEXEC_PATH to kde5 profile to fix drkonqi lookup

* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-3.20140519gita85f5bc
- Update to latest git snapshot
- Add PAM file
- Add profile.d entry

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> - 4.95.0-1.20140425git7c97c92
- Initial version of kde5-plasma-workspace

