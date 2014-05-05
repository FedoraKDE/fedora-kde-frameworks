#%define snapshot 20140205
%define framework kpty

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140505git985d14a1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 module providing Pty abstraction

License:        LGPL2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kpty-985d14a1.tar

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 tier 3 module providing Pty abstraction


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-ki18n-devel


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
%doc COPYING COPYING.LIB README.md
%{_kf5_libdir}/libKF5Pty.so.*

%files devel
%{_kf5_includedir}/kpty_version.h
%{_kf5_includedir}/KPty
%{_kf5_libdir}/libKF5Pty.so
%{_kf5_libdir}/cmake/KF5Pty
%{_kf5_archdatadir}/mkspecs/modules/qt_KPty.pri


%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140505git985d14a1
- Update to git: 985d14a1

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gitebdaacf4
- Update to git: ebdaacf4

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gitebdaacf4
- Update to git: ebdaacf4

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423gitd612e03c
- Update to git: d612e03c

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git9f012c62
- Update to git: 9f012c62

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

* Mon Jan  6 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
