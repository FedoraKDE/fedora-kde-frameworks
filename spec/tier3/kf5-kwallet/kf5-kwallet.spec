#%define snapshot 20140205
%define framework kwallet

Name:           kf5-%{framework}
Version:        4.98.0
Release:        4.20140425git67665f38%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for password management

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kwallet-67665f38.tar

BuildRequires:  libgcrypt-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kservice-devel


Requires:       kf5-kwallet-libs%{?_isa} = %{version}-%{release}
Requires:       kf5-kwallet-runtime%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 3 solution for password management.

%package        libs
Summary:        KWallet framework libraries
Requires:       kf5-filesystem
Provides:       kf5-kwallet-api%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-kwallet-api%{?_isa} < 4.98.0-3.20140422git388f0660
%description    libs
Provides API to access KWallet data from applications.

%package        runtime
Summary:        KWallet runtime deamon
Requires:       kf5-kded

%description    runtime
Provides a runtime deamon that stores passwords.

# FIXME: -devel can only depend on -api, otherwise we get circular  dependency
# problem, because -runtime depends on kf5-kded, which is not compiled at this point
# (kf5-kio requires kf5-kwallet, but kf5-kded requires kf5-kinit, which requires kf5-kio)
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

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

%files libs
%{_kf5_libdir}/libKF5Wallet.so.*
%{_kf5_libdir}/libkwalletbackend5.so.*

%files runtime
%{_kf5_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_kf5_bindir}/kwalletd5
%{_kf5_datadir}/kde5/services/kwalletd5.desktop
%{_kf5_datadir}/kwalletd/kwalletd.notifyrc

%files devel
%{_kf5_datadir}/dbus-1/interfaces/kf5_org.kde.KWallet.xml
%{_kf5_includedir}/kwallet_version.h
%{_kf5_includedir}/KWallet
%{_kf5_libdir}/cmake/KF5Wallet
%{_kf5_libdir}/libKF5Wallet.so
%{_kf5_libdir}/libkwalletbackend5.so
%{_kf5_archdatadir}/mkspecs/modules/qt_KWallet.pri

%changelog
* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425git67665f38
- Update to git: 67665f38

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140422git388f0660
- rename -api to -libs to follow naming conventions
- libkwalletbackend5 belongs to -libs, not -runtime

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140422git388f0660
- -devel can only Require -api, otherwise we have circular dependency problem

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git388f0660
- Update to git: 388f0660

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git388f0660
- Update to git: 388f0660

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git749c8a69
- Update to git: 749c8a69

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitab162784
- Update to git: ab162784

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
