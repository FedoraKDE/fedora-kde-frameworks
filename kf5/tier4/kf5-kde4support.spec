%define framework kde4support
%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.96.0
Release:        0.1.%{snapshot}git%{?dist}
Summary:        KDE Frameworks 5 Tier 4 module with porting aid from KDELibs 4
License:        LGPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-framework-%{version}.tar.xz


BuildRequires:  libX11-devel
BuildRequires:  libSM-devel
BuildRequires:  openssl-devel
BuildRequires:  gettext-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kdesignerplugin-devel
BuildRequires:  kf5-kglobalaccel-devel


%description
KDE Frameworks 5 Tier 4 module with porting aid from KDELibs 4


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
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
%{_kf5_bindir}/kf5-config
%{_kf5_libdir}/libKF5KDE4Support.so.*
%{_kf5_plugindir}/*.so
%{_kf5_qtplugindir}/designer/*.so
%{_kf5_libexecdir}/fileshareset
%{_kf5_libexecdir}/filesharelist
%{_kf5_mandir}/man1/kf5-config.1
%{_kf5_datadir}/kde5/services/*.protocol
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_datadir}/kde5/services/qimageioplugins/*.desktop
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_datadir}/locale/*
%{_kf5_datadir}/kf5widgets/
%{_kf5_datadir}/kssl/ca-bundle.crt
%{_kf5_sysconfdir}/xdg/*

%files devel
%{_kf5_libdir}/libKF5KDE4Support.so
%{_kf5_libdir}/cmake/KF5KDE4Support/
%{_kf5_libdir}/cmake/KDELibs4/
%{_kf5_includedir}/kde4support_version.h
%{_kf5_includedir}/KDE4Support/


%changelog
* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140206git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
