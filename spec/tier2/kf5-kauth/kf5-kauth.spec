#%define snapshot 20140205
%define framework kauth

Name:           kf5-%{framework}
Version:        4.98.0
Release:        3.20140428git9be07165%{?dist}
Summary:        KDE Frameworks 5 Tier 2 integration module to perform actions as privileged user

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kauth-9be07165.tar

Patch0:         kauth-find-polkit-qt5.patch

BuildRequires:  polkit-qt5-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-kcoreaddons-devel

Requires:       kf5-filesystem

%description
KAuth is a framework to let applications perform actions as a privileged user.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%patch0 -p1 -b .polkitqt5

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
%{_kf5_libdir}/libKF5Auth.so.*
%{_kf5_sysconfdir}/dbus-1/system.d/*
%{_kf5_plugindir}/kauth/helper/kauth_helper_plugin.so
%{_kf5_plugindir}/kauth/backend/kauth_backend_plugin.so
%{_kf5_datadir}/kauth/
%{_kf5_libexecdir}/kauth-policy-gen


%files devel
%{_kf5_includedir}/kauth_version.h
%{_kf5_includedir}/KAuth
%{_kf5_libdir}/libKF5Auth.so
%{_kf5_libdir}/cmake/KF5Auth
%{_kf5_archdatadir}/mkspecs/modules/qt_KAuth.pri


%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140428git9be07165
- Update to git: 9be07165

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428git9be07165
- Update to git: 9be07165

* Mon Apr 28 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-20140418git84a2c68a
- Rebuild against kf5-rpm-macros

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git84a2c68a
- Update to git: 84a2c68a

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Wed Jan 15 2014 Daniel Vr8til <dvratil@redhat.com> 4.95.0-2
- Rebuilt against polkit-qt5

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
