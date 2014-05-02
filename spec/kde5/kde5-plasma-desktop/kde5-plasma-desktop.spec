# %define snapshot  20140315

Name:           kde5-plasma-desktop
Version:        4.95.0
Release:        1.20140428git7046caa%{?dist}
Summary:        Plasma 2 desktop

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/kde-workspace.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/plasma/%{version}/kde-workspace-%{version}.tar.xz
Source0:        kde5-plasma-desktop-7046caa.tar

BuildRequires:  libusb-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kde5-plasma-workspace-devel
BuildRequires:  kde5-kwin-devel

# Optional
BuildRequires:  kf5-kactivities-libs-devel

Requires:       kde5-plasma-workspace
Requires:       kde5-filesystem

%description
Plasma 2 Desktop.

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
%setup -q -n plasma-desktop-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kde5_bindir}/*
%{_kde5_libdir}/*.so.*
%{_kde5_plugindir}/kf5/plasma/dataengine/*.so
%{_kde5_plugindir}/kf5/plasma/geolocationprovider/*.so
%{_kde5_plugindir}/kf5/plasma/packagestructure/*.so
%{_kde5_plugindir}/kf5/*.so
%{_kde5_plugindir}/kf5/plugins/phonon_platform/kde.so
%{_kde5_libdir}/qml/org/kde/*
%{_kde5_libdir}/kconf_update_bin
%{_kde5_libexecdir}/*
%{_kde5_datadir}/kde5/services/*.desktop
%{_kde5_datadir}/kde5/services/*.protocol
%{_kde5_datadir}/kde5/services/kded/*.desktop
%{_kde5_datadir}/kde5/servicetypes/*.desktop
%{_kde5_datadir}/applications/*.desktop
%{_kde5_datadir}/config.kcfg
%{_kde5_datadir}/kconf_update/*
%{_kde5_datadir}/ksmserver
%{_kde5_datadir}/ksplash
%{_kde5_datadir}/freespacenotifier
%{_kde5_datadir}/plasma/plasmoids
%{_kde5_datadir}/plasma/services
%{_kde5_datadir}/plasma/shareprovider
%{_kde5_datadir}/plasma/wallpapers
%{_kde5_datadir}/plasma/look-and-feel
%{_kde5_datadir}/solid
%{_kde5_datadir}/kstyle
%{_kde5_datadir}/dbus-1/services/*.service
%{_kde5_datadir}/desktop-directories/*.directory
%{_kde5_datadir}/drkonqi/debuggers/external/*
%{_kde5_datadir}/drkonqi/debuggers/internal/*
%{_kde5_datadir}/drkonqi/mappings
%{_kde5_datadir}/drkonqi/pics/*.png
%{_kde5_datadir}/phonon/phonon.notifyrc
%{_kde5_sysconfdir}/xdg/*.knsrc
%{_kde5_sysconfdir}/xdg/autostart/*.desktop

# %%{_datadir} here is intended - we need to install to location where DMs look
%{_datadir}/xsessions/kde5-plasma.desktop

%files doc
# %doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_kde5_datadir}/doc/HTML/en/*

%files devel
%{_kde5_libdir}/*.so
%{_kde5_libdir}/cmake/KRunnerAppDBusInterface
%{_kde5_libdir}/cmake/KSMServerDBusInterface
%{_kde5_libdir}/cmake/LibKWorkspace
%{_kde5_libdir}/cmake/LibTaskManager
%{_kde5_libdir}/cmake/ScreenSaverDBusInterface
%{_kde5_includedir}/*
%{_kde5_datadir}/dbus-1/interfaces/*.xml

# TODO split to subpackages
# - KCM (?)
# - plasmoids
# - icons
# - individual tools


%changelog
* Mon Apr 28 2014 Daniel Vrátil <dvratil@redhat.com> - 4.95.0-1.20140428git7046caa
- Initial version of kde5-plasma-desktop
