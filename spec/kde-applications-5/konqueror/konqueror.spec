%global git_date    20141024
%global git_commit  8a1c3ad

Name:           konqueror
Version:        4.97.0
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        KDE File Manager and Browser

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar.gz --remote=git://anongit.kde.org/kde-baseapps.git \
#             --output=kde-baseapps-%%{git_commit}.tar.gz \
#             --prefix=kde-baseapps-%%{git_commit}/ %%{git_commit}
Source0:        kde-baseapps-%{git_commit}.tar.gz

Patch0:         konqueror-standalone-build.patch

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-khtml-devel
BuildRequires:  kf5-kdelibs4support-devel

# Unstable
BuildRequires:  kf5-konq-devel

BuildRequires:  zlib-devel

Requires:       kf5-filesystem
Requires:       kio-extras

%description
Konqueror allows you to manage your files and browse the web in a
unified interface.

%package        libs
Summary:        Konqueror runtime libraries
%description    libs
%{summary}.


%prep
%setup -q -n kde-baseapps-%{git_commit}

%patch0 -p1 -b .stadaloneBuild

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../konqueror
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

rm %{buildroot}/%{_libdir}/libkonquerorprivate.so

%post 
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%files
%doc COPYING COPYING.DOC COPYING.LIB
%{_bindir}/konqueror
%{_libdir}/libkdeinit5_konqueror.so
%{_datadir}/applications/*.desktop
%{_datadir}/appdata/konqueror.appdata.xml
%{_datadir}/config.kcfg/konqueror.kcfg
%{_kf5_datadir}/kxmlgui5/konqueror
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/useragentstrings
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/kcontrol/pic/*.png
%{_datadir}/konqueror
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/icons/hicolor/*/*/*
%{_kf5_qtplugindir}/kcm_konq.so
%{_kf5_qtplugindir}/kcm_performance.so
%{_kf5_qtplugindir}/kcm_kio.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libkonquerorprivate.*

%changelog
* Fri Oct 24 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1.20141024git8a1c3ad
- Initial version
