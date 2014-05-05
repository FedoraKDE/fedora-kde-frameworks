#%define snapshot 20140206
%define framework knewstuff

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140505git25fd2aa5%{?dist}
Summary:        KDE Frameworks 5 Tier 3 module for downloading application assets

License:        LGPL2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-knewstuff-25fd2aa5.tar


BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kxmlgui-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 module for downloading application assets


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-karchive-devel
Requires:       kf5-kcompletion-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-ki18n-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-kio-devel
Requires:       kf5-kitemviews-devel
Requires:       kf5-ktextwidgets-devel
Requires:       kf5-kwidgetsaddons-devel
Requires:       kf5-kxmlgui-devel

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
%{_kf5_libdir}/libKF5NewStuff.so.*
%{_kf5_datadir}/knewstuff/

%files devel
%{_kf5_includedir}/knewstuff_version.h
%{_kf5_includedir}/KNewStuff3
%{_kf5_libdir}/libKF5NewStuff.so
%{_kf5_libdir}/cmake/KF5NewStuff
%{_kf5_archdatadir}/mkspecs/modules/qt_KNewStuff.pri


%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140505git25fd2aa5
- Update to git: 25fd2aa5

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gite715d88c
- Update to git: e715d88c

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gite715d88c
- Update to git: e715d88c

* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425gitab1e28d7
- Update to git: ab1e28d7

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git2d24aadf
- Update to git: 2d24aadf

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitff4cf19b
- Update to git: ff4cf19b

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
