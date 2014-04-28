#%define snapshot 20140205
%define framework kded

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140428git8cb9c5cf%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon with KDE Daemon

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kded-8cb9c5cf.tar

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-karchive-devel

Requires:       kf5-filesystem

%description
KDED stands for KDE Daemon which isn't very descriptive.
KDED runs in the background and performs a number of small tasks.
Some of these tasks are built in, others are started on demand.


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
%{_kf5_bindir}/kded5
%{_kf5_libdir}/libkdeinit5_kded5.so
%{_kf5_datadir}/dbus-1/services/*.service
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_mandir}/man8/*

%files devel
%{_kf5_libdir}/cmake/KDED
%{_kf5_datadir}/dbus-1/interfaces/*.xml


%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git8cb9c5cf
- Update to git: 8cb9c5cf

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git5a8445fb
- Update to git: 5a8445fb

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git5173dbb1
- Update to git: 5173dbb1

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git3015d1dc
- Update to git: 3015d1dc

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
