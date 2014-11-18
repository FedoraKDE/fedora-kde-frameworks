%global         git_date 20141026
%global         git_commit 2319d35

Name:           kcm_touchpad
Summary:        KDE Systemsettings module for touchpads
Version:        5.1.1
Release:        1.%{git_date}git%{git_commit}%{?dist}

License:        GPLv2+
Url:            https://projects.kde.org/kcm-touchpad

# git archive --format=tar.gz --remote=git://anongit.kde.org/kcm-touchpad.git \
#             --prefix=kcm-touchpad-%{version} --output=kcm-touchpad-%{git_commit}.tar.gz \
#             frameworks
Source0:        kcm-touchpad-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-kded-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-plasma-devel

BuildRequires:  pkgconfig
BuildRequires:  libxcb-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-drv-synaptics-devel
BuildRequires:  xorg-x11-server-devel

Requires:       kf5-filesystem


%description
%{summary}.


%prep
%setup -q -n kcm-touchpad-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags}  -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot}  -C %{_target_platform}

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files
%doc COPYING
%{_bindir}/kcm-touchpad-list-devices
%{_qt5_plugindir}/kded_touchpad.so
%{_qt5_plugindir}/plasma_engine_touchpad.so
%{_datadir}/config.kcfg/touchpad.kcfg
%{_datadir}/config.kcfg/touchpaddaemon.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.touchpad.xml
%{_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/knotifications5/kcm_touchpad.notifyrc
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kded/touchpad.desktop
%{_kf5_datadir}/plasma/desktoptheme/default/icons/touchpad.svg
%{_kf5_datadir}/plasma/plasmoids/touchpad
%{_kf5_datadir}/plasma/services/touchpad.operations


%changelog
* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Sun Oct 26 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-1.20141026git2319d35
- Initial version
