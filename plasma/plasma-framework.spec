%define snapshot  20140109

Name:           plasma-framework
Version:        5.0.0
Release:        0.1.%{snapshot}git
Summary:        Plasma 2 libraries and runtime components

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/%{name}.git master | \
# gzip -c > %{name}-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXext-devel
BuildRequires:  libSM-devel
BuildRequires:  openssl-devel
BuildRequires:  libGL-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtquick1-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtscript-devel

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
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kross-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kdnssd-devel

BuildRequires:  attica-qt5-devel
BuildRequires:  kactivities-qt5


%description
Plasma 2 libraries and runtime components


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

# TODO: Supackages!
# -shell
# -quick
# -wallpapers
# -plasmoids
# -icons (-desktopthemes?)


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_bindir}/plasmapkg
%{_kf5_bindir}/plasma-shell
%{_kf5_libdir}/libKF5Plasma.so.*
%{_kf5_libdir}/libKF5PlasmaQuick.so.*
%{_kf5_libdir}/platformqml/touch/org/kde/plasma
%{_kf5_libdir}/plugins/kf5/*.so
%{_kf5_libdir}/plugins/kf5/plasma/dataengine/*.so
%{_kf5_libdir}/qml/org/kde/*
%{_kf5_libdir}/qml/org/kde/*
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/desktoptheme/*
%{_kf5_datadir}/plasma/
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_datadir}/kde5/services/kded/*.desktop
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_sysconfdir}/xdg/autostart/plasma-shell.desktop


%files devel
%doc
%{_kf5_libdir}/cmake/KF5Plasma
%{_kf5_libdir}/cmake/KF5PlasmaQuick
%{_kf5_libdir}/libKF5Plasma.so
%{_kf5_libdir}/libKF5PlasmaQuick.so
%{_kf5_includedir}/plasma_version.h
%{_kf5_includedir}/plasma/
%{_kf5_includedir}/plasmaquick/
%{_kf5_includedir}/KDE/Plasma/
%{_kf5_includedir}/KDE/PlasmaQuick/



%changelog
* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
