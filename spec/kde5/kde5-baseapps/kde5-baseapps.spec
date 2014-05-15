%define git_commit 7c97c92
%define base_name kde-baseapps

Name:           kde5-baseapps
Version:        4.90.1
Release:        1.20140514git%{git_commit}%{?_dist}
Summary:        Collection of applications used for file and Internet browsing

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/kde-baseapps/%{version}/kde-baseapps-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

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
%{_kde5_bindir}/dolphin
%{_kde5_bindir}/kdialog
%{_kde5_bindir}/kfind
%{_kde5_bindir}/kdepasswd
%{_kde5_bindir}/servicemenuinstallation
%{_kde5_bindir}/servicemenudeinstallation
%{_kde5_plugindir}/*.so
%{_kde5_libdir}/libkonq.so.*
%{_kde5_libdir}/libdolphinprivate.so.*
%{_kde5_libdir}/libkdeinit4_dolphin.so
%{_kde5_datadir}/kbookmark/directory_bookmarkbar.desktop
%{_kde5_datadir}/kdm/
%{_kde5_datadir}/konqueror/
%{_kde5_datadir}/dolphin
%{_kde5_datadir}/dolphinpart
%{_datadir}/kservices5/
%{_datadir}/kservicetypes5/
%{_datadir}/templates/
%{_datadir}/applications/
%{_datadir}/config.kcfg/
%{_datadir}/dbus-1/
%{_datadir}/icons/hicolor/
%{_kde5_sysconfdir}/xdg/servicemenu.knsrc

%files devel
%{_kde5_includedir}/*.h
%{_kde5_libdir}/libkonq.so
%{_kde5_libdir}/libdolphinprivate.so

%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> 4.90.1-1.20140514git7c97c92
- Update to latest git snapshot

* Mon May 05 2014 Jan Grulich <jgrulich@redhat.com> 4.90.1-1.20140505git
- initial version
