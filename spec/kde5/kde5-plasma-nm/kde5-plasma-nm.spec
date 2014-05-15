%global         git_commit 9cc2530
%global         base_name plasma-nm

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1%{?dist}
Summary:        Plasma Next applet written in QML for managing network connections
License:        LGPLv2+ and GPLv2+
URL:            https://projects.kde.org/projects/playground/network/plasma-nm
#Source0:        http://download.kde.org/unstable/plasma-nm//plasma-nm-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

# Add plasma-nm to default systray if needed, for upgraders...
Source10: 01-fedora-plasma-nm.js

## upstream patches
#Patch0:   openconnect.patch
#Patch1:   item-text.patch

BuildRequires:  gettext

BuildRequires:  kde5-filesystem
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qttools-devel


BuildRequires:  kf5-modemmanagerqt-devel
BuildRequires:  kf5-networkmanagerqt-devel

BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
BuildRequires:  pkgconfig(ModemManager) >= 1.0.0
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)
%if 0%{?fedora} || 0%{?epel}
BuildRequires:  pkgconfig(openconnect) >= 4.00
%endif

Requires:  NetworkManager >= 0.9.8
Requires:  kf5-networkmanagerqt

Obsoletes: kde-plasma-networkmanagement < 1:0.9.1.0
Obsoletes: kde-plasma-networkmanagement-libs < 1:0.9.1.0
Provides:  kde-plasma-networkmanagement = 1:%{version}-%{release}
Provides:  kde-plasma-networkmanagement-libs = 1:%{version}-%{release}

%description
Plasma applet and editor for managing your network connections in KDE 4 using
the default NetworkManager service.

# Required for properly working GMS/CDMA connections
%package mobile
Summary: Mobile support for %{name}
Requires:  ModemManager
Requires:  mobile-broadband-provider-info
Requires:  libmm-qt5 >= 1.0.0
Obsoletes: kde-plasma-networkmanagement-mobile < 1:0.9.1.0
Provides:  kde-plasma-networkmanagement-mobile = 1:%{version}-%{release}
%description mobile
%{summary}.

%if 0%{?fedora} || 0%{?epel}
%package openvpn
Summary:        OpenVPN support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openvpn
Obsoletes:      kde-plasma-networkmanagement-openvpn < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-openvpn = 1:%{version}-%{release}
%description openvpn
%{summary}.

%package vpnc
Summary:        Vpnc support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-vpnc
Obsoletes:      kde-plasma-networkmanagement-vpnc < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-vpnc = 1:%{version}-%{release}
%description vpnc
%{summary}.

%package openconnect
Summary:        OpenConnect support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openconnect
Obsoletes:      kde-plasma-networkmanagement-openconnect < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-openconnect = 1:%{version}-%{release}
%description openconnect
%{summary}.

%package openswan
Summary:        Openswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openswan
%description openswan
%{summary}.

%package strongswan
Summary:        Strongswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       strongswan
%description strongswan
%{summary}.

%package l2tp
Summary:        L2TP support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-l2tp
%description l2tp
%{summary}.

%package pptp
Summary:        PPTP support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-pptp
Obsoletes:      kde-plasma-networkmanagement-pptp < 1:0.9.1.0
Provides:       kde-plasma-networkmanagement-pptp = 1:%{version}-%{release}
%description pptp
%{summary}.
%endif

%prep
%setup -qn plasma-nm-%{version}

#%patch0 -p1 -b .openconnect
#%patch1 -p1 -b .item-text

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

#%find_lang plasma_applet_org.kde.networkmanagement
#%find_lang plasmanetworkmanagement-kded
#%find_lang kde-nm-connection-editor
#%find_lang libplasmanetworkmanagement-editor
#%find_lang plasmanetworkmanagement_vpncui
#%find_lang plasmanetworkmanagement_openvpnui
#%find_lang plasmanetworkmanagement_openconnectui
#%find_lang plasmanetworkmanagement_openswanui
#%find_lang plasmanetworkmanagement_strongswanui
#%find_lang plasmanetworkmanagement_l2tpui
#%find_lang plasmanetworkmanagement_pptpui

# migrate to nm plasmoid
install -m644 -p -D %{SOURCE10} %{buildroot}%{_datadir}/plasma/updates/01-fedora-plasma-nm.js

%post
touch --no-create %{_kde5_iconsdir}/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde5_iconsdir}/oxygen &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde5_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde5_iconsdir}/oxygen &> /dev/null || :
fi

#%files -f plasma_applet_org.kde.networkmanagement.lang -f plasmanetworkmanagement-kded.lang -f kde-nm-connection-editor.lang -f libplasmanetworkmanagement-editor.lang
%files
%defattr(-,root,root,-)
# kde-nm-connection-editor
%{_kde5_bindir}/kde-nm-connection-editor
%{_kde5_libdir}/libplasmanetworkmanagement-editor.so
%{_kde5_datadir}/kde-nm-connection-editor/kde-nm-connection-editorui.rc
%{_datadir}/applications/kde-nm-connection-editor.desktop
# plasma-nm applet
%{_kde5_libdir}/qml/org/kde/plasma/networkmanagement/libplasmanetworkmanagementplugins.so
%{_kde5_libdir}/qml/org/kde/plasma/networkmanagement/qmldir
%dir %{_kde5_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/
%{_kde5_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/contents
%{_kde5_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/metadata.desktop
%{_datadir}/kservices5/plasma-applet-org.kde.plasma.networkmanagement.desktop
#%{_kde5_ndir}/plugins/kf5/plugins/designer/libplasmanetworkmanagementwidgets.so
#%{_kde5_appsdir}/desktoptheme/default/icons/plasma-networkmanagement2.svgz
%{_datadir}/plasma/updates/*.js
# plasma-nm notifications
#%{_kde5_datadir}/kservices5/networkmanagement_notifications.desktop
#%{_kde5_libdir}/plugins/kf5/networkmanagement_notifications.so
%{_datadir}/knotifications5/networkmanagement.notifyrc
# plasma-nm kded
%{_kde5_plugindir}/kded_networkmanagement.so
%{_datadir}/kservices5/kded/networkmanagement.desktop
# plasma-nm other
%{_kde5_libdir}/libplasmanetworkmanagement-internal.so
%{_datadir}/kservicetypes5/plasma-networkmanagement-vpnuiplugin.desktop


%files mobile

%if 0%{?fedora} || 0%{?epel}
#%files openvpn -f plasmanetworkmanagement_openvpnui.lang
%files openvpn
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_openvpnui.so
%{_datadir}/kservices5/plasmanetworkmanagement_openvpnui.desktop

#%files vpnc -f plasmanetworkmanagement_vpncui.lang
%files vpnc
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_vpncui.so
%{_datadir}/kservices5/plasmanetworkmanagement_vpncui.desktop

#%files openconnect -f plasmanetworkmanagement_openconnectui.lang
%files openconnect
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_openconnectui.so
%{_datadir}/kservices5/plasmanetworkmanagement_openconnectui.desktop

#%files openswan -f plasmanetworkmanagement_openswanui.lang
%files openswan
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_openswanui.so
%{_datadir}/kservices5/plasmanetworkmanagement_openswanui.desktop

#%files strongswan -f plasmanetworkmanagement_strongswanui.lang
%files strongswan
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_strongswanui.so
%{_datadir}/kservices5/plasmanetworkmanagement_strongswanui.desktop

#%files l2tp -f plasmanetworkmanagement_l2tpui.lang
%files l2tp
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_l2tpui.so
%{_datadir}/kservices5/plasmanetworkmanagement_l2tpui.desktop

#%files pptp -f plasmanetworkmanagement_pptpui.lang
%files pptp
%{_kde5_plugindir}/plasmanetworkmanagement/vpnuiplugin/libplasmanetworkmanagement_pptpui.so
%{_datadir}/kservices5/plasmanetworkmanagement_pptpui.desktop
%endif

%changelog
* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git9cc2530
- fork into kde5-plasma-nm
