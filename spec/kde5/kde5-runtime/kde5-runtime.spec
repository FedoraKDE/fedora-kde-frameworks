%define snapshot  20140315

Name:           kde5-runtime
Version:        4.95.0
Release:        1%{?dist}
Summary:        Core runtime for KDE 5

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/kde-runtime/%{version}/kde-runtime-%{version}.tar.xz

#Patch0:         kde5-runtime-kioexec-crash.patch

# udev
BuildRequires:  openslp-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  samba-devel
BuildRequires:  libssh-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  exiv2-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtquick1-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  phonon-qt5-devel
BuildRequires:  alsa-lib-devel

BuildRequires:  kde5-filesystem
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kitemmodels-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-threadweaver-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kross-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-knotifyconfig-devel
BuildRequires:  kf5-kemoticons-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kde4support-devel
BuildRequires:  kf5-kdesignerplugin-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kpty-devel
BuildRequires:  kf5-kdewebkit-devel
BuildRequires:  kf5-kdnssd-devel

Requires:       oxygen-icon-theme >= 4.11.0
Requires:       dbus-x11

Requires:       kf5-kded

# drkonqi
Requires:       polkit

Provides:       dbus-notification-daemon

%description
KDE core runtime components

%prep
%setup -q -n kde-runtime-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} .. -DCMAKE_MODULE_PATH:PATH=%{_kf5_datadir}/ECM/find-modules
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING COPYING.LIB
%{_kde5_bindir}/kuiserver
%{_kde5_bindir}/ktrash
%{_kde5_bindir}/kcmshell5
%{_kde5_bindir}/kioclient
%{_kde5_bindir}/kde4-menu
%{_kde5_bindir}/kdeopen
%{_kde5_bindir}/kdecp
%{_kde5_bindir}/kdemv
%{_kde5_bindir}/ktraderclient
%{_kde5_bindir}/kdebugdialog
%{_kde5_bindir}/keditfiletype
%{_kde5_bindir}/kfile5
%{_kde5_bindir}/khelpcenter
%{_kde5_bindir}/khotnewstuff4
%{_kde5_bindir}/kmimetypefinder
%{_kde5_bindir}/kreadconfig
%{_kde5_bindir}/ksvgtopng
%{_kde5_bindir}/kwriteconfig
%{_kde5_bindir}/kglobalaccel5
%{_kde5_bindir}/kstart
%{_kde5_libexecdir}/drkonqi
%{_kde5_libexecdir}/kdeeject
%{_kde5_libexecdir}/kdesu
%{_kde5_libexecdir}/khc_docbookdig.pl
%{_kde5_libexecdir}/khc_htdig.pl
%{_kde5_libexecdir}/khc_htsearch.pl
%{_kde5_libexecdir}/khc_indexbuilder
%{_kde5_libexecdir}/khc_mansearch.pl
%{_kde5_libexecdir}/knetattach
%{_kde5_libdir}/libkdeinit5_*.so
%{_kde5_libdir}/kconf_update_bin/phonon*
%{_kde5_libdir}/libmolletnetwork.so
%{_kde5_libdir}/libmolletnetwork.so.*
%{_kde5_plugindir}/kf5/kded_*.so
%{_kde5_plugindir}/kf5/kcm_*.so
%{_kde5_plugindir}/kf5/kio_*.so
%{_kde5_plugindir}/kf5/jpegthumbnail.so
%{_kde5_plugindir}/kf5/imagethumbnail.so
%{_kde5_plugindir}/kf5/kcmspellchecking.so
%{_kde5_plugindir}/kf5/fixhosturifilter.so
%{_kde5_plugindir}/kf5/kurisearchfilter.so
%{_kde5_plugindir}/kf5/kuriikwsfilter.so
%{_kde5_plugindir}/kf5/kshorturifilter.so
%{_kde5_plugindir}/kf5/localdomainurifilter.so
%{_kde5_plugindir}/kf5/plugins/phonon_platform/kde.so
%{_kde5_plugindir}/kf5/libkmanpart.so

%{_kde5_datadir}/applications/*.desktop
%{_kde5_datadir}/desktop-directories/*.directory
%{_kde5_datadir}/icons/hicolor/*/*
%{_kde5_datadir}/khelpcenter/
%{_kde5_datadir}/config.kcfg/*.kcfg
%{_kde5_datadir}/dbus-1/services/*.service
%{_kde5_datadir}/dbus-1/interfaces/*.xml
%{_kde5_datadir}/drkonqi/
%{_kde5_datadir}/kcm_componentchooser/*.desktop
%{_kde5_datadir}/kcmlocale/
%{_kde5_datadir}/locale/currency/
%{_kde5_datadir}/locale/l10n/
%{_kde5_datadir}/sounds/
%{_kde5_datadir}/kconf_update/*.upd
%{_kde5_datadir}/libphonon/hardwaredatabase
%{_kde5_datadir}/kcm_phonon/
%{_kde5_datadir}/phonon/phonon.notifyrc
%{_kde5_datadir}/kde5/services/*.desktop
%{_kde5_datadir}/kde5/services/*.protocol
%{_kde5_datadir}/kde5/services/kded/*.desktop
%{_kde5_datadir}/kde5/services/searchproviders/*.desktop
%{_kde5_datadir}/kde5/servicetypes/*.desktop
%{_kde5_datadir}/kglobalaccel/
%{_kde5_datadir}/konqueror/dirtree/remote/smb-network.desktop
%{_kde5_datadir}/konqsidebartng/virtual_folders/remote/virtualfolder_network.desktop
%{_kde5_datadir}/ksmserver/windowmanagers/*.desktop
%{_kde5_datadir}/remoteview/
%{_kde5_datadir}/doc/
%{_kde5_datadir}/man/
%{_kde5_datadir}/kio_*
%{_kde5_datadir}/mime/packages/network.xml
%{_kde5_sysconfdir}/xdg/*.knsrc
%{_kde5_sysconfdir}/xdg/menus/kde-information.menu
%{_kde5_sysconfdir}/xdg/kshorturifilterrc

# TODO Add subpackages:
# - drkonqi
# - kio-smb


%changelog
* Wed Apr 02 2014 Daniel Vrátíl <dvratil@redhat.com> 4.95.0-1
- update to KDE Runtime 4.95.0 (Alpha 1)

* Sat Mar 15 2014 Jan Grulich <jgrulich@redhat.com 4.90.1-6.20140315git
- update git snapshot

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-5.20140213git
- update to latest git snapshot

* Sat Feb 08 2014 Martin Briza <mbriza@redhat.com> 4.90.1-4.20140116git
- prevent annoying errors on package removing

* Mon Jan 20 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-3.20140116git
- apply workaround for kioexec crash

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-2.20140116git
- require oxygen-icon-theme 4.11.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-1.20140116git
- initial version
