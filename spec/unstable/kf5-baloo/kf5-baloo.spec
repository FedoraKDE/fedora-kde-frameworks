%define         framework baloo
%define         git_commit 46e3ea7
Name:           kf5-%{framework}
Version:        4.90.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 module that provides indexing and search functionality

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
#Source0:        %{framework}-%{git_commit}.tar.xz
Source0:        baloo-%{git_commit}.tar.xz

Patch0:         baloo-mime.patch
Patch1:         baloo-fix-build.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-akonadi-devel
BuildRequires:  akonadi-qt5-devel
BuildRequires:  kf5-kfilemetadata-devel
BuildRequires:  xapian-core-devel
BuildRequires:  kf5-kabc-devel
BuildRequires:  kf5-kmime-devel
BuildRequires:  kf5-kpimutils-devel
BuildRequires:  kf5-akonadi-kmime-devel

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{framework}-%{version}

%patch0 -p1 -b .mime
%patch1 -p1 -b .build

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../ \
         -DKDEPIM_SUPPORT_BUILD:BOOL=ON \
         -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
         -DKF5_INCLUDE_INSTALL_DIR=/usr/include/KF5
# FIXME: Remove ^^ once fixed upstream
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libbaloocore.so.*
%{_kf5_libdir}/libbalooxapian.so.*
%{_kf5_libdir}/libbaloofiles.so.*
%{_kf5_libdir}/libbaloopim.so.*
%{_kf5_plugindir}/baloo_filesearchstore.so
%{_kf5_plugindir}/baloo_emailsearchstore.so
%{_kf5_plugindir}/baloo_contactsearchstore.so
%{_kf5_plugindir}/libbaloo_notesearchstore.so
%{_kf5_plugindir}/akonadi/akonadi_baloo_searchplugin.so
%{_kf5_plugindir}/akonadi/akonadibaloosearchplugin.desktop
%{_kf5_plugindir}/krunner_baloosearchrunner.so
%{_kf5_plugindir}/kcm_baloofile.so
%{_kf5_bindir}/baloo_file
%{_kf5_bindir}/baloo_file_extractor
%{_kf5_bindir}/baloo_file_cleaner
%{_kf5_bindir}/akonadi_baloo_indexer
%{_kf5_bindir}/baloosearch
%{_kf5_bindir}/balooshow
%{_kf5_sysconfdir}/xdg/autostart/baloo_file.desktop
%{_kf5_sysconfdir}/dbus-1/system.d/org.kde.baloo.filewatch.conf
%{_kf5_libexecdir}/kde_baloo_filewatch_raiselimit
%{_kf5_datadir}/dbus-1/system-services/org.kde.baloo.filewatch.service
%{_kf5_datadir}/kservicetypes5/baloosearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_filesearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_emailsearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_contactsearchstore.desktop
%{_kf5_datadir}/kservices5/baloo_notesearchstore.desktop
%{_kf5_datadir}/kservices5/kcm_baloofile.desktop
%{_kf5_datadir}/kservices5/plasma-runner-baloosearch.desktop
%{_kf5_datadir}/polkit-1/actions/org.kde.baloo.filewatch.policy
%{_kf5_datadir}/akonadi/agents/akonadibalooindexingagent.desktop
%{_kf5_datadir}/icons/hicolor/*/apps/baloo.png


%files devel
%{_kf5_libdir}/libbaloocore.so
%{_kf5_libdir}/libbaloofiles.so
%{_kf5_libdir}/libbaloopim.so
%{_kf5_libdir}/libbalooxapian.so

%{_kf5_libdir}/cmake/Baloo
%{_includedir}/baloo
%{_kf5_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml


%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-1.20140514git46e3ea7
- KF5 Baloo 4.90.0 (git snapshot built from common kdepimlibs/frameworks repo)
