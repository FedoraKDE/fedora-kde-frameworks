#%define snapshot 20140205
%define framework kglobalaccel

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140422gitb5c1bc5d%{?dist}
Summary:        KDE Frameworks 5 Tier 1 integration module for global shortcuts

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kglobalaccel-b5c1bc5d.tar

BuildRequires:  libX11-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

Requires:       kf5-filesystem

%description
KDE Framework 5 Tier 1 integration module for global shortcuts


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
%{_kf5_libdir}/libKF5GlobalAccel.so.*

%files devel
%doc
%{_kf5_includedir}/kglobalaccel_version.h
%{_kf5_includedir}/KGlobalAccel/
%{_kf5_libdir}/libKF5GlobalAccel.so
%{_kf5_datadir}/dbus-1/interfaces/*
%{_kf5_libdir}/cmake/KF5GlobalAccel
%{_kf5_archdatadir}/mkspecs/modules/qt_KGlobalAccel.pri


%changelog
* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422gitb5c1bc5d
- Update to git: b5c1bc5d

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git8cdf7054
- Update to git: 8cdf7054

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
