Name:           kio-extras
Version:        5.0.0
Release:        2%{?dist}
Summary:        Additional components to increase the functionality of KIO Framework

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

Patch0:         kio-extras-install-dirs.patch

BuildRequires:  kf5-rpm-macros

BuildRequires:  qt5-qtbase-devel
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kdnssd-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-solid-devel

BuildRequires:  phonon-qt5-devel
BuildRequires:  openslp-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libssh-devel
BuildRequires:  bzip2-devel
BuildRequires:  exiv2-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  lzma-devel

Requires:       kf5-filesystem

%description
%{summary}.

%package        docs
Summary:        Documentation and user manuals for %{name}
Obsoletes:      kde-runtime-docs < 5.0.0-1
Requires:       %{name} = %{version}-%{release}
%description    docs
%{summary}.

%prep
%setup -q

%patch0 -p1 -b .installdirs

%build

sed -e "s/PO_FILES //" -i po/*/CMakeLists.txt

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang kioextras5 --with-qt --all-name

# Remove libmolletnetwork.so - we don't have headers for it anyway and having
# a -devel package just because of this does not make sense
rm %{buildroot}/%{_libdir}/libmolletnetwork.so

%files -f kioextras5.lang
%{_bindir}/ktrash5
%{_libdir}/libmolletnetwork.so.*
%{_kf5_plugindir}/kio/*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_plugindir}/parts/*.so
%{_kf5_qtplugindir}/*.so
%{_datadir}/kio_desktop
%{_datadir}/kio_docfilter
%{_datadir}/kio_bookmarks
%{_datadir}/kio_info
%{_datadir}/konqsidebartng/virtual_folders/remote/virtualfolder_network.desktop
%{_datadir}/konqueror/dirtree/remote/smb-network.desktop
%{_datadir}/remoteview
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/thumbcreator.desktop
%{_datadir}/dbus-1/interfaces/kf5_org.kde.network.kioslavenotifier.xml
%{_datadir}/mime/packages/kf5_network.xml
%{_datadir}/config.kcfg/jpegcreatorsettings.kcfg

%files docs
%{_datadir}/doc/HTML/en/kioslave5
%{_datadir}/doc/HTML/en/kcontrol



%changelog
* Tue Jul 29 2014 Daniel Vrátil <dvratil@redhat.cim> - 5.0.0-2
- Split -docs to improve coinstallability with KDE 4

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514gitf7a2bbe
- Initial version
