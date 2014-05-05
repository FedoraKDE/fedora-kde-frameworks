%define snapshot  20140505

Name:           kde5-baseapps
Version:        4.90.1
Release:        0.1.%{snapshot}git%{?dist}
Summary:        Collection of applications used for file and Internet browsing

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/kde-baseapps/%{version}/kde-baseapps-%{version}.tar.xz
Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  zlib-devel

BuildRequires:  kde5-filesystem
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kactivities-libs-devel

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n kde-baseapps-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} .. -DCMAKE_MODULE_PATH:PATH=%{_kf5_datadir}/ECM/find-modules
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc COPYING COPYING.LIB
%{_kde5_bindir}/kdepasswd
%{_kde5_bindir}/kdialog
%{_kde5_bindir}/kfind
%{_kde5_libdir}/plugins/
%{_kde5_libdir}/libkonq.so.*
%{_kde5_datadir}/templates/
%{_kde5_datadir}/applications/
%{_kde5_datadir}/config.kcfg/
%{_kde5_datadir}/dbus-1/
%{_kde5_datadir}/icons/hicolor/
%{_kde5_datadir}/kbookmark/directory_bookmarkbar.desktop
%{_kde5_datadir}/kdm/
%{_kde5_datadir}/konqueror/
%{_kde5_datadir}/kservices5/
%{_kde5_datadir}/kservicetypes5/

%files devel
%{_kde5_includedir}/*
%{_kde5_libdir}/libkonq.so

%changelog
* Mon May 05 2014 Jan Grulich <jgrulich@redhat.com> 4.90.1-1.20140505git
- initial version
