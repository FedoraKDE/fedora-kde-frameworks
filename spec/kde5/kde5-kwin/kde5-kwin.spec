#%define snapshot 20140205
%define git_commit 61c631c
%define base_name kwin

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        KDE Window manager

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qttools-static

BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kdoctools-devel

# Optional
BuildRequires:  kf5-kactivities-libs-devel
BuildRequires:  kf5-kdoctools-devel

Requires:       kde5-filesystem
Requires:       qt5-qtmultimedia

%description
KCompletion provides widgets with advanced completion support as well as a
lower-level completion class which can be used with your own widgets.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-devel
Requires:       kf5-kwidgetsaddons-devel
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        USer manual for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    doc
%{summary}.


%prep
%setup -q -n kwin-%{version}

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
%doc COMPLIANCE COPYING COPYING.DOC HACKING README
%{_kde5_bindir}/kwin
%{_kde5_datadir}/kwin
%{_kde5_libdir}/libkdeinit5_kwin.so
%{_kde5_libdir}/libkdeinit5_kwin_rules_dialog.so
%{_kde5_libdir}/libkdecorations.so.*
%{_kde5_libdir}/libkwinxrenderutils.so.*
%{_kde5_libdir}/libkwineffects.so.*
%{_kde5_libdir}/libkwinglutils.so.*
%{_kde5_libdir}/libkwin4_effect_builtins.so.*
%{_kde5_libdir}/plugins/*.so
%{_kde5_libdir}/plugins/kwin
%{_kde5_libdir}/qml/org/kde/kwin
%{_kde5_libdir}/kconf_update_bin/kwin5_update_default_rules
%{_kde5_libexecdir}/kwin_killer_helper
%{_kde5_libexecdir}/kwin_rules_dialog
%{_kde5_datadir}/kwincompositing
%{_datadir}/kservices5/*.desktop
%{_datadir}/kservices5/kwin
%{_datadir}/kservicetypes5/*.desktop
%{_datadir}/knotifications5/kwin.notifyrc
%{_datadir}/config.kcfg/kwin.kcfg
%{_datadir}/icons/oxygen/*/actions/*
%{_kde5_sysconfdir}/xdg/*.knsrc

%files doc
%doc COMPLIANCE COPYING COPYING.DOC HACKING README
%{_datadir}/doc/HTML/en/kcontrol/*

%files devel
%{_libdir}/cmake/KWinDBusInterface
%{_libdir}/cmake/KDecorations
%{_datadir}/dbus-1/interfaces/*.xml
%{_kde5_libdir}/libkdecorations.so
%{_kde5_libdir}/libkwinxrenderutils.so
%{_kde5_libdir}/libkwineffects.so
%{_kde5_libdir}/libkwinglutils.so
%{_kde5_libdir}/libkwin4_effect_builtins.so
%{_kde5_includedir}/*.h



%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1.20140514git61c631c
- Update to latest upstream git snapshot

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1.20140425gitb92f4a6
- Initial package
