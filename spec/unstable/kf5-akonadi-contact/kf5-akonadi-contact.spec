%global         framework akonadi-contact
%global         git_commit dda3e7d
Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library with API to access contacts in Akonadi

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# Source0:        http://download.kde.org/unstable/networkmanagement/%{version}/src/%{name}-%{version}.tar.xz
# # Package from git snapshots using releaseme scripts
#Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz
#Source0:        %{framework}-%{git_commit}.tar.xz
Source0:        kdepimlibs-frameworks-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  phonon-qt5-devel
BuildRequires:  akonadi-qt5-devel
BuildRequires:  kf5-kabc-devel
BuildRequires:  kf5-akonadi-devel
BuildRequires:  kf5-akonadi-kmime-devel
BuildRequires:  kf5-kcalcore-devel
BuildRequires:  kf5-kmime-devel
BuildRequires:  kf5-kpimutils-devel

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-akonadi-devel
Requires:       kf5-kabc-devel
Requires:       kf5-kcalcore-devel
Requires:       kf5-kmime-devel
Requires:       kf5-kpimutils-devel
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-kio-devel
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn kdepimlibs-%{version}

%build
mkdir -p %{_target_platform}/%{framework}
pushd %{_target_platform}/%{framework}
%{cmake_kf5} ../../%{framework} \
         -DINCLUDE_INSTALL_DIR:PATH=/usr/include \
         -DKF5_INCLUDE_INSTALL_DIR=/usr/include/KF5
# FIXME: Remove ^^ once fixed upstream
popd

make %{?_smp_mflags} -C %{_target_platform}/%{framework}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}/%{framework}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5AkonadiContact.so.*
%{_kf5_plugindir}/kcm_akonadicontact_actions.so
%{_kf5_datadir}/kf5/akonadi/contact
%{_kf5_datadir}/config.kcfg/recentcontactscollections.kcfg
%{_kf5_datadir}/kservices5/akonadicontact_actions.desktop
%{_kf5_datadir}/kservices5/akonadi/contact
%{_kf5_datadir}/kservicetypes5/kaddressbookimprotocol.desktop

%files devel
%{_kf5_libdir}/libKF5AkonadiContact.so
%{_kf5_libdir}/cmake/KF5AkonadiContact
%{_kf5_includedir}/Akonadi/Contact
%{_kf5_includedir}/akonadi-contact_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiContact.pri

%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-1.20140514gitdda3e7d
- KF5 Akonadi Contact 4.98.0 (git snapshot built from common kdepimlibs/frameworks repo)
