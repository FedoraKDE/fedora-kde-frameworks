#%define snapshot 20140205
%define framework kdesu

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140505gitecf00213%{?dist}
Summary:        KDE Frameworks 5 Tier 3 module for su integration

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kdesu-ecf00213.tar

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kpty-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 module for su integration


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
%{_kf5_libdir}/libKF5Su.so.*
%{_kf5_libexecdir}/kdesu_stub
%{_kf5_libexecdir}/kdesud

%files devel
%doc
%{_kf5_includedir}/kdesu_version.h
%{_kf5_includedir}/KDESu
%{_kf5_libdir}/libKF5Su.so
%{_kf5_libdir}/cmake/KF5Su
%{_kf5_archdatadir}/mkspecs/modules/qt_KDESu.pri


%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140505gitecf00213
- Update to git: ecf00213

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gita905dd84
- Update to git: a905dd84

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gita905dd84
- Update to git: a905dd84

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git825a134f
- Update to git: 825a134f

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gita278d106
- Update to git: a278d106

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
