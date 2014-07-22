%define         framework baloo

Name:           kf5-%{framework}
Version:        5.0.0
Release:        2%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 module that provides indexing and search functionality

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{framework}-%{version}.tar.xz

Patch0:         baloo-kioslaves-install.patch
Patch1:         baloo-stores-install.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kfilemetadata-devel
BuildRequires:  xapian-core-devel

BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-krunner-devel

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kfilemetadata-devel
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{framework}-%{version}

%patch0 -p1 -b .kioslaves
%patch1 -p1 -b .stores

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../ 
#\
#         -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
#         -DKF5_INCLUDE_INSTALL_DIR=/usr/include/KF5
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang baloo_qt5 --with-qt --all-name

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f baloo_qt5.lang
%{_kf5_libdir}/libKF5BalooCore.so.*
%{_kf5_libdir}/libKF5BalooXapian.so.*
%{_kf5_libdir}/libKF5BalooFiles.so.*
%{_kf5_plugindir}/baloo/filesearchstore.so
%{_kf5_plugindir}/baloo/emailsearchstore.so
%{_kf5_plugindir}/baloo/contactsearchstore.so
%{_kf5_plugindir}/baloo/notesearchstore.so
%{_kf5_plugindir}/baloo/calendarsearchstore.so
%{_kf5_plugindir}/kio/baloosearch.so
%{_kf5_plugindir}/kio/tags.so
%{_kf5_plugindir}/kio/timeline.so
%{_kf5_qtplugindir}/kcm_baloofile.so
%{_kf5_bindir}/baloo_file
%{_kf5_bindir}/baloo_file_extractor
%{_kf5_bindir}/baloo_file_cleaner
%{_kf5_bindir}/baloosearch
%{_kf5_bindir}/balooshow
%{_kf5_bindir}/balooctl
%{_kf5_sysconfdir}/xdg/autostart/baloo_file.desktop
%{_kf5_sysconfdir}/dbus-1/system.d/org.kde.baloo.filewatch.conf
%{_kf5_libexecdir}/kauth/kde_baloo_filewatch_raiselimit
%{_kf5_datadir}/dbus-1/system-services/org.kde.baloo.filewatch.service
%{_kf5_datadir}/kservicetypes5/baloosearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_filesearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_emailsearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_contactsearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_notesearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_calendarsearchstore.desktop
%{_kf5_datadir}/kservices5/kcm_baloofile.desktop
%{_kf5_datadir}/kservices5/baloosearch.protocol
%{_kf5_datadir}/kservices5/tags.protocol
%{_kf5_datadir}/kservices5/timeline.protocol
%{_kf5_datadir}/polkit-1/actions/org.kde.baloo.filewatch.policy
%{_kf5_datadir}/icons/hicolor/*/apps/baloo.png


%files devel
%{_kf5_libdir}/libKF5BalooCore.so
%{_kf5_libdir}/libKF5BalooXapian.so
%{_kf5_libdir}/libKF5BalooFiles.so

%{_kf5_libdir}/cmake/KF5Baloo
%{_kf5_includedir}/Baloo
%{_kf5_includedir}/baloo_version.h
%{_kf5_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml


%changelog
* Tue Jul 22 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- -devel Requires kf5-kfilemetadata-devel
- does not obsolete baloo < 5.0.0 (coinstallability)

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-3.20140611git84bc23c
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-2.20140611git46e3ea7
- KF5 Baloo 4.90.0 (git snapshot built from common kdepimlibs/frameworks repo)
