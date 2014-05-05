#%define snapshot 20140205
%define framework kcrash

Name:           kf5-%{framework}
Version:        4.98.0
Release:        3.20140505git389de5e9%{?dist}
Summary:        KDE Frameworks 5 Tier 2 addon for application crashes

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kcrash-389de5e9.tar

Patch0:         kcrash-find-drkonqi-in-path.patch

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kf5-filesystem

%description
KCrash provides support for intercepting and handling application crashes.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kwindowsystem-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%patch0 -p1 -b .drkonqi-path

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
%{_kf5_libdir}/libKF5Crash.so.*

%files devel
%{_kf5_includedir}/kcrash_version.h
%{_kf5_includedir}/KCrash
%{_kf5_libdir}/libKF5Crash.so
%{_kf5_libdir}/cmake/KF5Crash
%{_kf5_archdatadir}/mkspecs/modules/qt_KCrash.pri

%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140505git389de5e9
- Update to git: 389de5e9

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-3.20140428git0c24964b
- Update to git: 0c24964b

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428git0c24964b
- Update to git: 0c24964b

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git9c2fc626
- Update to git: 9c2fc626

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git9e87a146
- Update to git: 9e87a146

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-2
- Forgot to include patch for drkonqi

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Mon Mar 24 2014 Daniel Vrátil <dvratil@redhat.com> 4.97.0-2
- Add patch for KCrash to look for drkonqi in $PATH

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- Rebuild against new kf5-filesystem

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
