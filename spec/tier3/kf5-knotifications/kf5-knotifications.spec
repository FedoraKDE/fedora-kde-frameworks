#%define snapshot 20140205
%define framework knotifications

Name:           kf5-%{framework}
Version:        4.99.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 2 solution for notifications

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/4.99.0/%{framework}-4.99.0.tar.xz

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  phonon-qt5-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kcoreaddons-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 2 solution for notifications

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kwindowsystem-devel
Requires:       kf5-kservice-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-kcodecs-devel
Requires:       kf5-kcoreaddons-devel

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
%find_lang knotifications5_qt --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f knotifications5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5Notifications.so.*

%files devel
%{_kf5_includedir}/knotifications_version.h
%{_kf5_includedir}/KNotifications
%{_kf5_libdir}/libKF5Notifications.so
%{_kf5_libdir}/cmake/KF5Notifications
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_archdatadir}/mkspecs/modules/qt_KNotifications.pri


%changelog
* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Fri Feb 07 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.2.20140205git
- Rebuild against kwindowsystem

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
