%global git_date    20141024
%global git_commit  30844aa

Name:           gwenview
Version:        4.97.0
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        An image viewer

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar.gz --remote=git://anongit.kde.org/gwenview.git \
#             --output=gwenview-%%{git_commit}.tar.gz \
#             --prefix=gwenview-%%{git_commit}/ %%{git_commit}
Source0:        gwenview-%{git_commit}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtsvg-devel

BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kactivities-devel

# Plasma
BuildRequires:  kf5-baloo-devel

BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  exiv2-devel
BuildRequires:  lcms2-devel

#BuildRequires:  libkdcraw-devel

Requires:       kf5-filesystem


%description
%{summary}.

%package        libs
Summary:        Gwenview runtime libraries
%description    libs
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# Avoid -devel package
rm %{buildroot}/%{_libdir}/libgwenviewlib.so

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%files
%doc COPYING COPYING.DOC
%{_bindir}/gwenview
%{_kf5_qtplugindir}/gvpart.so
%{_kf5_datadir}/kxmlgui5/gwenview
%{_kf5_datadir}/kservices5/ServiceMenus/slideshow.desktop
%{_kf5_datadir}/kservices5/gvpart.desktop
%{_datadir}/applications/gwenview.desktop
%{_datadir}/appdata/gwenview.appdata.xml
%{_datadir}/gwenview
%{_datadir}/gvpart
%{_datadir}/doc/HTML/*/gwenview
%{_datadir}/icons/hicolor/*/*/*

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libgwenviewlib.so.*


%changelog
* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-20141024git30844aa
- Initial version 
