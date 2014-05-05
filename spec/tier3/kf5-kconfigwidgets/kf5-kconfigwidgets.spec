#%define snapshot 20140205
%define framework kconfigwidgets

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140505git7234537f%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon for creating configuration dialogs

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kconfigwidgets-7234537f.tar

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwidgetsaddons-devel

Requires:       kf5-filesystem

%description
KConfigWidgets provides easy-to-use classes to create configuration dialogs, as
well as a set of widgets which uses KConfig to store their settings.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kauth-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kcodecs-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kdoctools-devel
Requires:       kf5-kguiaddons-devel
Requires:       kf5-ki18n-devel
Requires:       kf5-kwidgetsaddons-devel

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
%{_kf5_libdir}/libKF5ConfigWidgets.so.*
%{_kf5_bindir}/preparetips5
%{_kf5_datadir}/kconfigwidgets
%{_kf5_mandir}/man1/*

%files devel
%doc
%{_kf5_includedir}/kconfigwidgets_version.h
%{_kf5_includedir}/KConfigWidgets
%{_kf5_libdir}/libKF5ConfigWidgets.so
%{_kf5_libdir}/cmake/KF5ConfigWidgets
%{_kf5_archdatadir}/mkspecs/modules/qt_KConfigWidgets.pri


%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140505git7234537f
- Update to git: 7234537f

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428git8c785479
- Update to git: 8c785479

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git8c785479
- Update to git: 8c785479

* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425git79f9feb8
- Update to git: 79f9feb8

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422gitd9168c6e
- Update to git: d9168c6e

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git86479300
- Update to git: 86479300

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
