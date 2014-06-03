#%define snapshot 20140206
%define framework attica


Name:           kf5-attica
Version:        4.100.0
Release:        1%{?dist}
Summary:        KDE Frameworks Tier 1 Addon with Open Collaboration Services API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/attica,git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2

Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

Requires:       kf5-filesystem

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.4.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
%{summary}.


%prep
%setup -q -n %{framework}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README.md
%doc ChangeLog
%{_kf5_libdir}/libKF5Attica.so.*

%files devel
%{_kf5_libdir}/cmake/KF5Attica/
%{_kf5_includedir}/attica_version.h
%{_kf5_includedir}/Attica/
%{_kf5_libdir}/libKF5Attica.so
%{_kf5_archdatadir}/mkspecs/modules/qt_Attica.pri
%{_kf5_libdir}/pkgconfig/libKF5Attica.pc


%changelog
* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Tue May 06 2014 Daniel Vrátil <dvratil@redhat.com>
- Rebuild against updated kf5-rpm-macros

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-2
- Remove Provides and Obsoletes (not needed in actual repos)

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-20140206git
- Attica is now a proper Tier 1 framework

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 1.0.0-20140205git
- Update snapshot of Attica to current git

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 1.0.0-1
- Update to KDE Frameworks 5 TP1 (4.9.95)

* Mon Jan 06 2014 Daniel Vrátil <dvratil@redhat.com> 0.4.2-1
- Attica-qt5 4.9.95 - fork attica to attica-qt5
