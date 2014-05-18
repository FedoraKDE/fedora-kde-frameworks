%define base_name konsole
%define git_commit 57a5f23

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        0.20140515git%{git_commit}%{?dist}
Summary:        Konsole is a terminal program for KDE 5

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

# udev

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kitemmodels-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kross-devel
BuildRequires:  kf5-kde4support-devel
BuildRequires:  kf5-kdoctools-devel

Requires:       kde5-filesystem

%description
Konsole is a terminal program for KDE 5.

%prep
%setup -q -n %{base_name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README
%{_kde5_bindir}/konsole
%{_kde5_bindir}/konsoleprofile
%{_kde5_libdir}/libkdeinit5_konsole.so
%{_kde5_libdir}/libkonsoleprivate.so
%{_kde5_plugindir}/konsolepart.so
%{_kde5_datadir}/konsole
%{_kde5_datadir}/kconf_update/*
%{_datadir}/applications/org.kde.konsole.desktop
%{_datadir}/kservicetypes5/terminalemulator.desktop
%{_datadir}/kservices5/konsolepart.desktop
%{_datadir}/kservices5/ServiceMenus/*.desktop
%{_datadir}/knotifications5/konsole.notifyrc
%{_datadir}/doc/HTML/en/konsole/


%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-20140515git57a5f23
- Updated to latest git snapshot

* Fri Feb 07 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-0.1.20140213git
- Initial version
