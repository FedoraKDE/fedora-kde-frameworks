#%define snapshot 20140205
%define framework kxmlgui

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140505gitd0b18e53%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for generating UI

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kxmlgui-d0b18e53.tar

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-sonnet-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for generating UI


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
%doc COPYING COPYING.LIB README.md
%{_kf5_libdir}/libKF5XmlGui.so.*
%{_kf5_sysconfdir}/xdg/ui/ui_standards.rc
%{_kf5_libexecdir}/ksendbugmail
%{_kf5_datadir}/kxmlgui/

%files devel
%{_kf5_includedir}/kxmlgui_version.h
%{_kf5_includedir}/KXmlGui
%{_kf5_libdir}/libKF5XmlGui.so
%{_kf5_libdir}/cmake/KF5XmlGui
%{_kf5_archdatadir}/mkspecs/modules/qt_KXmlGui.pri


%changelog
* Mon May 05 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140505gitd0b18e53
- Update to git: d0b18e53

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-2.20140428gitb0270b17
- Update to git: b0270b17

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gitb0270b17
- Update to git: b0270b17

* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425git4779adee
- Update to git: 4779adee

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git2a7c6811
- Update to git: 2a7c6811

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git9998609c
- Update to git: 9998609c

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418giteeb0e399
- Update to git: eeb0e399

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
