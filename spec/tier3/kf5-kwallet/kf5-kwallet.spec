#%define snapshot 20140205
%define framework kwallet

Name:           kf5-%{framework}
Version:        5.3.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for password management

License:        LGPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/stable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libgcrypt-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-runtime%{?_isa} = %{version}-%{release}

%description
KWallet is a secure and unified container for user passwords.

%package        libs
Summary:        KWallet framework libraries
Requires:       kf5-filesystem
%description    libs
Provides API to access KWallet data from applications.

%package        runtime
Summary:        KWallet runtime deamon

%description    runtime
Provides a runtime deamon that stores passwords.

# FIXME: -devel can only depend on -api, otherwise we get circular  dependency
# problem, because -runtime depends on kf5-kded, which is not compiled at this point
# (kf5-kio requires kf5-kwallet, but kf5-kded requires kf5-kinit, which requires kf5-kio)
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-devel
Requires:       kf5-kwindowsystem-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kdbusaddons-devel
Requires:       kf5-ki18n-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-knotifications-devel
Requires:       kf5-kservice-devel
Requires:       kf5-kwidgetsaddons-devel
Requires:       kf5-kwindowsystem-devel

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
%find_lang kwalletd5_qt --with-qt --all-name

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md

%files libs
%{_kf5_libdir}/libKF5Wallet.so.*
%{_kf5_libdir}/libkwalletbackend5.so.*

%files runtime -f kwalletd5_qt.lang
%{_kf5_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_kf5_datadir}/dbus-1/services/org.kde.kwalletd.service
%{_kf5_bindir}/kwalletd5
%{_kf5_datadir}/kservices5/kwalletd5.desktop
%{_kf5_datadir}/knotifications5/kwalletd.notifyrc

%files devel
%{_kf5_datadir}/dbus-1/interfaces/kf5_org.kde.KWallet.xml
%{_kf5_includedir}/kwallet_version.h
%{_kf5_includedir}/KWallet
%{_kf5_libdir}/cmake/KF5Wallet
%{_kf5_libdir}/libKF5Wallet.so
%{_kf5_libdir}/libkwalletbackend5.so
%{_kf5_archdatadir}/mkspecs/modules/qt_KWallet.pri

%changelog
* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Mon Sep 15 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Tue Jun 24 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-2
- Fix %%post and %%postun
- Removed kf5-kded from Requires to avoid circular dependency

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-3
- Fix Provides/Obsoletes

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140422git388f0660
- rename -api to -libs to follow naming conventions
- libkwalletbackend5 belongs to -libs, not -runtime

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140422git388f0660
- -devel can only Require -api, otherwise we have circular dependency problem

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
