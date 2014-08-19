Name:           plasma-nm
Version:        5.0.1
Release:        1%{?dist}
Summary:        Plasma Next applet written in QML for managing network connections
License:        LGPLv2+ and GPLv2+
URL:            https://projects.kde.org/projects/playground/network/plasma-nm

Source0:        http://download.kde.org/stable/plasma/5.0.0/%{name}-%{version}.tar.xz

# Add plasma-nm to default systray if needed, for upgraders...
Source10: 01-fedora-plasma-nm.js

## upstream patches
#Patch0:   openconnect.patch
#Patch1:   item-text.patch

BuildRequires:  gettext

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qttools-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-libmm-qt-devel
BuildRequires:  kf5-libnm-qt-devel

BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
BuildRequires:  pkgconfig(ModemManager) >= 1.0.0
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)
%if 0%{?fedora} || 0%{?epel}
BuildRequires:  pkgconfig(openconnect) >= 4.00
%endif

Requires:  NetworkManager >= 0.9.8

Requires:  kf5-filesystem

Obsoletes: kde-plasma-networkmanagement < 1:0.9.1.0
Obsoletes: kde-plasma-networkmanagement-libs < 1:0.9.1.0
Obsoletes: kde-plasma-nm < 5.0.0-1

%description
Plasma applet and editor for managing your network connections in KDE 4 using
the default NetworkManager service.

# Required for properly working GMS/CDMA connections
%package mobile
Summary: Mobile support for %{name}
Requires:  ModemManager
Requires:  mobile-broadband-provider-info
Requires:  kf5-libmm-qt >= 5.0.0-1
Obsoletes: kde-plasma-networkmanagement-mobile < 1:0.9.1.0
Obsoletes: kde-plasma-nm-mobile < 5.0.0-1
%description mobile
%{summary}.

%if 0%{?fedora} || 0%{?epel}
%package openvpn
Summary:        OpenVPN support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openvpn
Obsoletes:      kde-plasma-networkmanagement-openvpn < 1:0.9.1.0
Obsoletes:      kde-plasma-nm-openvpn < 5.0.0-1
%description openvpn
%{summary}.

%package vpnc
Summary:        Vpnc support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-vpnc
Obsoletes:      kde-plasma-networkmanagement-vpnc < 1:0.9.1.0
Obsoletes:      kde-plasma-nm-vpnc < 5.0.0-1
%description vpnc
%{summary}.

%package openconnect
Summary:        OpenConnect support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openconnect
Obsoletes:      kde-plasma-networkmanagement-openconnect < 1:0.9.1.0
Obsoletes:      kde-plasma-nm-openconnect < 5.0.0-1

%description openconnect
%{summary}.

%package openswan
Summary:        Openswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-openswan
Obsoletes:      kde-plasma-nm-openswan < 5.0.0-1
%description openswan
%{summary}.

%package strongswan
Summary:        Strongswan support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       strongswan
Obsoletes:      kde-plasma-nm-strongswan < 5.0.0-1
%description strongswan
%{summary}.

%package l2tp
Summary:        L2TP support for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-l2tp
Obsoletes:      kde-plasma-nm-l2tp < 5.0.0-1
%description l2tp
%{summary}.

%package pptp
Summary:        PPTP support for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release} 
Requires:       NetworkManager-pptp
Obsoletes:      kde-plasma-networkmanagement-pptp < 1:0.9.1.0
Obsoletes:      kde-plasma-nm-pptp < 5.0.0-1
%description pptp
%{summary}.
%endif

%prep
%setup -q

#%patch0 -p1 -b .openconnect
#%patch1 -p1 -b .item-text

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang plasma_applet_org.kde.plasma.networkmanagement
%find_lang plasmanetworkmanagement-kded
%find_lang kde5-nm-connection-editor
%find_lang plasmanetworkmanagement-libs
%find_lang plasmanetworkmanagement_vpncui
%find_lang plasmanetworkmanagement_openvpnui
%find_lang plasmanetworkmanagement_openconnectui
%find_lang plasmanetworkmanagement_openswanui
%find_lang plasmanetworkmanagement_strongswanui
%find_lang plasmanetworkmanagement_l2tpui
%find_lang plasmanetworkmanagement_pptpui

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

%files -f plasma_applet_org.kde.plasma.networkmanagement.lang -f plasmanetworkmanagement-kded.lang -f kde5-nm-connection-editor.lang -f plasmanetworkmanagement-libs.lang
%files
# kde-nm-connection-editor
%{_bindir}/kde5-nm-connection-editor
%{_libdir}/libplasmanm_internal.so
%{_libdir}/libplasmanm_editor.so
%{_kf5_datadir}/kxmlgui5/kde5-nm-connection-editor/kde5-nm-connection-editorui.rc
%{_datadir}/applications/kde5-nm-connection-editor.desktop
# plasma-nm applet
%{_qt5_prefix}/qml/org/kde/plasma/networkmanagement/libplasmanm_qmlplugins.so
%{_qt5_prefix}/qml/org/kde/plasma/networkmanagement/qmldir
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/
%{_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/contents
%{_datadir}/plasma/plasmoids/org.kde.plasma.networkmanagement/metadata.desktop
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.plasma.networkmanagement.desktop
%{_datadir}/plasma/updates/*.js
# plasma-nm notifications
%{_kf5_datadir}/knotifications5/networkmanagement.notifyrc
# plasma-nm kded
%{_kf5_qtplugindir}/kded_networkmanagement.so
%{_kf5_datadir}/kservices5/kded/networkmanagement.desktop
# plasma-nm other
%{_kf5_datadir}/kservicetypes5/plasma-networkmanagement-vpnuiplugin.desktop


%files mobile

%if 0%{?fedora} || 0%{?epel}
%files openvpn -f plasmanetworkmanagement_openvpnui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_openvpnui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_openvpnui.desktop

%files vpnc -f plasmanetworkmanagement_vpncui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_vpncui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_vpncui.desktop

%files openconnect -f plasmanetworkmanagement_openconnectui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_openconnectui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_openconnectui.desktop

%files openswan -f plasmanetworkmanagement_openswanui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_openswanui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_openswanui.desktop

%files strongswan -f plasmanetworkmanagement_strongswanui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_strongswanui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_strongswanui.desktop

%files l2tp -f plasmanetworkmanagement_l2tpui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_l2tpui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_l2tpui.desktop

%files pptp -f plasmanetworkmanagement_pptpui.lang
%{_kf5_qtplugindir}/libplasmanetworkmanagement_pptpui.so
%{_kf5_datadir}/kservices5/plasmanetworkmanagement_pptpui.desktop
%endif

%changelog
* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0-1

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git9cc2530
- fork into kde5-plasma-nm
