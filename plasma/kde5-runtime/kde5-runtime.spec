%define snapshot  20140116

Name:           kde5-runtime
Version:        4.90.1
Release:        3.%{snapshot}git%{?dist}
Summary:        Core runtime for KDE 5

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}-%{snapshot}/ \
#             --remote=git://anongit.kde.org/%{name}.git framework | \
# bzip2 -c > %{name}-%{version}-%{snapshot}.tar.bz2
Source0:        %{name}-%{version}-%{snapshot}.tar.bz2

Patch0:         kde5-runtime-kioexec-crash.patch

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

BuildRequires:  plasma-framework-devel
BuildRequires:  attica-qt5-devel

Requires:       oxygen-icon-theme >= 4.11.0
Requires:       dbus-x11

Requires:       kf5-kded

# drkonqi
Requires:       polkit

Provides:       dbus-notification-daemon

%description
KDE core runtime components

%prep
%setup -q -n %{name}-%{version}-%{snapshot}

%patch0 -p1 -b .kioexec

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

# TODO Add subpackages:
# - drkonqi
# - kio-smb

%files
%doc COPYING COPYING.LIB
%{_kf5_bindir}/kglobalaccel
%{_kf5_bindir}/kuiserver
%{_kf5_bindir}/ktrash
%{_kf5_bindir}/kcmshell5
%{_kf5_bindir}/kioclient
%{_kf5_bindir}/kdeopen
%{_kf5_bindir}/kdecp
%{_kf5_bindir}/kdemv
%{_kf5_bindir}/ktraderclient
%{_kf5_libexecdir}/drkonqi
%{_kf5_libexecdir}/kioexec
%{_kf5_libdir}/libkdeinit5_*.so
%{_kf5_plugindir}/kded_*.so
%{_kf5_plugindir}/kcm_*.so
%{_kf5_plugindir}/kio_*.so
%{_kf5_plugindir}/jpegthumbnail.so
%{_kf5_plugindir}/imagethumbnail.so
%{_kf5_plugindir}/kcmspellchecking.so

%{_kf5_datadir}/config.kcfg/jpegcreatorsettings.kcfg
%{_kf5_datadir}/dbus-1/services/*.service
%{_kf5_datadir}/desktop-directories/kde-information.directory
%{_kf5_datadir}/drkonqi/
%{_kf5_datadir}/kcm_componentchooser/*.desktop
%{_kf5_datadir}/kcmlocale/
%{_kf5_datadir}/kconf_update/*.upd
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_datadir}/kde5/services/*.protocol
%{_kf5_datadir}/kde5/services/kded/*.desktop
%{_kf5_datadir}/kde5/servicetypes/thumbcreator.desktop
%{_kf5_datadir}/kglobalaccel/
%{_kf5_datadir}/konqueror/dirtree/remote/smb-network.desktop
%{_kf5_datadir}/ksmserver/windowmanagers/*.desktop
%{_kf5_datadir}/remoteview/
%{_kf5_sysconfdir}/xdg/*.knsrc
%{_kf5_sysconfdir}/xdg/menus/kde-information.menu


%changelog
* Mon Jan 20 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-3.20140116git
- apply workaround for kioexec crash

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-2.20140116git
- require oxygen-icon-theme 4.11.0

* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-1.20140116git
- initial version
