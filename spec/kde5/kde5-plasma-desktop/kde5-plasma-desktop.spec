%define         git_commit 532fc47
%define         base_name plasma-desktop

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140515git%{git_commit}%{?dist}
Summary:        Plasma 2 desktop

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/kde-workspace.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/plasma/%{version}/kde-workspace-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

Patch0:         plasma-desktop-fix-build.patch

BuildRequires:  libusb-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libX11-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-devel
BuildRequires:  libxkbcommon-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  phonon-qt5-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-ksysguard-devel
BuildRequires:  kde5-plasma-workspace-devel
BuildRequires:  kde5-kwin-devel

# Optional
BuildRequires:  kf5-kactivities-libs-devel
BuildRequires:  libcanberra-devel

BuildRequires:  chrpath

Requires:       kde5-plasma-workspace
Requires:       kde5-filesystem


%description
Plasma 2 Desktop.

%package        doc
Summary:        Documentation and user manuals for %{name}

%description    doc
Documentation and user manuals for %{name}.


%prep
%setup -q -n %{base_name}-%{version}

%patch0 -R -p1 -b .fixbuild

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

chrpath --delete %{buildroot}/%{_kde5_libdir}/qml/org/kde/plasma/private/kicker/libkickerplugin.so
chrpath --delete %{buildroot}/%{_kde5_libdir}/qml/org/kde/plasma/private/kickoff/libkickoffplugin.so
chrpath --delete %{buildroot}/%{_kde5_libdir}/qml/org/kde/plasma/private/taskmanager/libtaskmanagerplugin.so
chrpath --delete %{buildroot}/%{_kde5_libdir}/qml/org/kde/plasma/private/pager/libpagerplugin.so
chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_smserver.so

# No -devel
rm %{buildroot}/%{_kde5_libdir}/libkfontinst{,ui}.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kde5_bindir}/kapplymousetheme
%{_kde5_bindir}/kaccess
%{_kde5_bindir}/kfontinst
%{_kde5_bindir}/kfontview
%{_kde5_bindir}/krdb
%{_kde5_libexecdir}/kcmdatetimehelper
%{_kde5_libexecdir}/fontinst
%{_kde5_libexecdir}/fontinst_helper
%{_kde5_libexecdir}/fontinst_x11
%{_kde5_libexecdir}/kfontprint
%{_kde5_libexecdir}/knetattach
%{_kde5_libdir}/qml/org/kde/plasma/private
%{_kde5_libdir}/attica_kde.so
%{_kde5_libdir}/libkdeinit5_kaccess.so
%{_kde5_libdir}/kconf_update_bin/*
%{_kde5_libdir}/libkfontinst.so.*
%{_kde5_libdir}/libkfontinstui.so.*
%{_kde5_plugindir}/*.so
%{_kde5_datadir}/plasma/*
%{_kde5_datadir}/kcminput
%{_kde5_datadir}/color-schemes
%{_kde5_datadir}/kconf_update/*
%{_kde5_datadir}/kthememanager
%{_kde5_datadir}/kdisplay
%{_kde5_datadir}/kcontrol
%{_kde5_datadir}/kcmkeys
%{_kde5_datadir}/kcm_componentchooser
%{_kde5_datadir}/kcmlocale
%{_kde5_datadir}/kcm_phonon
%{_kde5_datadir}/kfontinst
%{_kde5_datadir}/kfontview
%{_kde5_datadir}/kcmkeyboard
%{_kde5_datadir}/ksmserver
%{_kde5_datadir}/konqsidebartng/virtual_folders/services/fonts.desktop
%{_kde5_sysconfdir}/dbus-1/system.d/*.conf
%{_kde5_sysconfdir}/xdg/*.knsrc
%{_datadir}/kservices5/*.desktop
%{_datadir}/kservices5/ServiceMenus/installfont.desktop
%{_datadir}/kservices5/fonts.protocol
%{_datadir}/kservices5/kded/*.desktop
%{_datadir}/knotifications5/*.notifyrc
%{_datadir}/icons/*/*/*/*
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/*.policy



%files doc
# %doc COPYING COPYING.DOC COPYING.LIB README README.pam
%{_datadir}/doc/HTML/en/*


%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git532fc47
- Initial version of kde5-plasma-desktop
