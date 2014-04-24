# %define snapshot  20140315
%define framework plasma

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140424git7ce31b6b%{?dist}
Summary:        KDE Frameworks 5 Tier 3 framework with Plasma 2 libraries and runtime components

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-plasma-7ce31b6b.tar

Provides:       plasma-framework
Obsoletes:      plasma-framework

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
# FIXME: Why do I need to isntall all backends when depending on QtSql?
BuildRequires:  qt5-qtbase-ibase
BuildRequires:  qt5-qtbase-odbc
BuildRequires:  qt5-qtbase-mysql
BuildRequires:  qt5-qtbase-postgresql
BuildRequires:  qt5-qtbase-tds

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kactivities-libs-devel
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
BuildRequires:  kf5-kdoctools-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 module with Plasma 2 libraries and runtime components


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

# TODO: Subpackages!
# -shell
# -quick
# -wallpapers
# -plasmoids
# -icons (-desktopthemes?)


%prep
#%setup -q -n %{framework}-framework-%{version}
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_bindir}/dpitest
%{_kf5_bindir}/plasmapkg2
%{_kf5_libdir}/libKF5Plasma.so.*
%{_kf5_libdir}/libKF5PlasmaQuick.so.*
%{_qt5_prefix}/platformqml/touch/org/kde/plasma
%{_kf5_qmldir}/org/kde/*
%{_kf5_qtplugindir}/kf5/*.so
%{_kf5_qtplugindir}/kf5/plasma/dataengine/
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/desktoptheme/*
%{_kf5_datadir}/plasma/
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_datadir}/kde5/services/kded/*.desktop
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_datadir}/plasma_scriptengine_ruby/data_engine.rb
${_kf5_mandir}/man1/plasmapkg2.1.gz

%files devel
%doc
%{_kf5_libdir}/cmake/KF5Plasma
%{_kf5_libdir}/cmake/KF5PlasmaQuick
%{_kf5_libdir}/libKF5Plasma.so
%{_kf5_libdir}/libKF5PlasmaQuick.so
%{_kf5_includedir}/plasma_version.h
%{_kf5_includedir}/plasma/
%{_kf5_includedir}/Plasma/


%changelog
* Thu Apr 24 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140424git7ce31b6b
- Update to git: 7ce31b6b

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git0ef526b8
- Update to git: 0ef526b8

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422gite1a25552
- Update to git: e1a25552

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git1d5c6e59
- Update to git: 1d5c6e59

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422gitac1e50d3
- Update to git: ac1e50d3

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git16ea0c68
- Update to git: 16ea0c68

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git709d60a7
- Update to git: 709d60a7

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Sat Mar 15 2014 Jan Grulich <jgrulich@redhat.com 4.97.0-3.20140315git
- update git snapshot

* Wed Mar 12 2014 Jan Grulich <jgrulich@redhat.com 4.97.0-2.20140312git
- update to git snapshot

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1
- upgrade to Tier 3 Framework kf5-plasma

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
