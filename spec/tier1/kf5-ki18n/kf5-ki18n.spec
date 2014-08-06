#%define snapshot 20140205
%define framework ki18n

Name:           kf5-%{framework}
Version:        5.1.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon for localization

License:        LGPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/stable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  perl

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  gettext

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 1 addon for localization.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gettext

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
%find_lang ki18n5_qt --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f ki18n5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5I18n.so.*
%{_kf5_qtplugindir}/kf5/ktranscript.so


%files devel
%{_kf5_includedir}/ki18n_version.h
%{_kf5_includedir}/KI18n
%{_kf5_libdir}/libKF5I18n.so
%{_kf5_libdir}/cmake/KF5I18n
%{_kf5_archdatadir}/mkspecs/modules/qt_KI18n.pri

%changelog
* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Thu Jul 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Remove obsolete upstream patch

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Mon Jun 09 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-2
- add upstream patch to fix plugins installation destination

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.100.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-4
- Rebuild against updated kf5-rpm-macros

* Thu May 08 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-3
- BR gettext

* Tue May 06 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-2
- Rebuild against updated kf5-rpm-macros

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Tue Apr 22 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-2
- Upgrade KI18n to a Tier 1 Framework

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
