#%define snapshot 20140205
%define framework kinit

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140425git346f375a%{?dist}
Summary:        KDE Frameworks 5 tier 3 solution for process launching

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kinit-346f375a.tar

Patch0:         kinit-respect-env-paths.patch

BuildRequires:  libX11-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-karchive-devel

Requires:       kf5-filesystem

%description
kdeinit is a process launcher somewhat similar to the
famous init used for booting UNIX.

It launches processes by forking and then loading a
dynamic library which should contain a 'kdemain(...)'
function.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{framework}-%{version}

%patch0 -p1 -b .env-paths

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
%{_kf5_bindir}/*
%{_kf5_libdir}/libkdeinit5_klauncher.so
%{_kf5_libexecdir}/*
%{_kf5_mandir}/man8/kdeinit5.8.gz

%files devel
%{_kf5_libdir}/cmake/KF5Init
%{_kf5_datadir}/dbus-1/interfaces/*.xml


%changelog
* Fri Apr 25 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140425git346f375a
- Update to git: 346f375a

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423gitaa682aeb
- Update to git: aa682aeb

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git044617f0
- Update to git: 044617f0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Mon Mar 24 2014 Daniel Vrátil <dvratil@redhat.com> 4.97.0-2
- Add patch for kinit to respect PATH and LD_LIBRARY_PATH

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rebuild against updated kf5-filesytem

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
