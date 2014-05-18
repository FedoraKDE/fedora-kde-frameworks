%define base_name    kio-extras
%define git_commit   f7a2bbe

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        Additional components to increase the functionality of KIO Framework

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  kde5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
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

%description
%{summary}.

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

# Remove libmolletnetwork.so - we don't have headers for it anyway and having
# a -devel package just because of this does not make sense
rm %{buildroot}/%{_kde5_libdir}/libmolletnetwork.so

%files
%{_kde5_bindir}/ktrash5
%{_kde5_libdir}/libmolletnetwork.so.*
%{_kde5_plugindir}/*.so
%{_kde5_datadir}/kio_desktop
%{_kde5_datadir}/kio_docfilter
%{_kde5_datadir}/kio_bookmarks
%{_kde5_datadir}/kio_info
%{_kde5_datadir}/konqsidebartng/virtual_folders/remote/virtualfolder_network.desktop
%{_kde5_datadir}/konqueror/dirtree/remote/smb-network.desktop
%{_kde5_datadir}/remoteview
%{_datadir}/kservices5/*.protocol
%{_datadir}/kservices5/*.desktop
%{_datadir}/kservices5/kded/*.desktop
%{_datadir}/kservicetypes5/thumbcreator.desktop
%{_datadir}/dbus-1/interfaces/kf5_org.kde.network.kioslavenotifier.xml
%{_datadir}/mime/packages/kf5_network.xml
%{_datadir}/doc/HTML/en/kioslave5
%{_datadir}/doc/HTML/en/kcontrol
%{_datadir}/config.kcfg/jpegcreatorsettings.kcfg


%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514gitf7a2bbe
- Initial version
