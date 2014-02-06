%define framework frameworkintegration
%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.96.0
Release:        0.1.%{snapshot}git%{?dist}
Summary:        KDE Frameworks 5 Tier 4 addon with framework integration
License:        LGPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-framework-%{version}.tar.xz


BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-karchive-devel

%description
Framework Integration is a set of plugins responsible for better integration of
Qt applications when running on a KDE Plasma workspace.

Applications do not need to link to this directly.


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
%{_kf5_libdir}/libKF5Style.so.*
%{_kf5_datadir}/kf5/infopage/*
%{_kf5_qtplugindir}/kf5/FrameworkIntegrationPlugin.so
%{_kf5_qtplugindir}/platformthemes/KDEPlatformTheme.so

%files devel
%{_kf5_includedir}/kstyle_version.h
%{_kf5_includedir}/KStyle
%{_kf5_libdir}/libKF5Style.so
%{_kf5_libdir}/cmake/KF5Style


%changelog
* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140206git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.9.95)

* Wed Jan 8 2014 Lukáš Tinkl <ltinkl@redhat.com>
- initial version
