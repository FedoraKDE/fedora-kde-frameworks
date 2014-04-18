#%define snapshot 20140205
%define framework kdewebkit

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 integration module for WebKit

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz


BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kjobwidgets-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 integration module for WebKit


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
%{_kf5_libdir}/libKF5WebKit.so.*

%files devel
%{_kf5_includedir}/kdewebkit_version.h
%{_kf5_includedir}/KDEWebKit
%{_kf5_libdir}/libKF5WebKit.so
%{_kf5_libdir}/cmake/KF5WebKit
%{_kf5_archdatadir}/mkspecs/modules/qt_KDEWebKit.pri

%changelog
* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
