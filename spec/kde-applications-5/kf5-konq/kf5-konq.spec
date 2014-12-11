%define         framework  konq
%define         git_commit 8a1c3ad
%define         git_date   20141024

Name:           kf5-%{framework}
Version:        4.97.0
Release:        2.%{git_date}git%{git_commit}%{?dist}
Summary:        KDE Frameworks Library with LibKonq shared resources.

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org

# git archive --format=tar.gz --remote=git://anongit.kde.org/kde-baseapps.git \
#             --output=kde-baseapps-%%{git_commit}.tar.gz \
#             --prefix=kde-baseapps-%%{git_commit}/ %%{git_commit}
Source0:        kde-baseapps-%{git_commit}.tar.gz

Patch0:         konq-install-konq_popupmenu.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kdelibs4support-devel

BuildRequires:  zlib-devel

Obsoletes:      libkonq%{_isa} < 4.9.7.0
Provides:       libkonq%{?_isa} = %{version}-%{release}

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-kxmlgui-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kio-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kservice-devel
Requires:       kf5-kparts-devel
Obsoletes:      libkonq-devel%{?_isa} < 4.9.70
Provides:       libkonq-devel%{?_isa} = %{version}-%{release}
Provides:       libkonq-devel = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n kde-baseapps-%{git_commit}

%patch0 -p1 -b .installHeader

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../lib/konq
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5Konq.so.*
%{_kf5_qtplugindir}/kded_favicons.so
%{_kf5_datadir}/kf5/kbookmark/*.desktop
%{_kf5_datadir}/kf5/konqueror/pics/*.png
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/kservices5/kded/favicons.desktop
%{_datadir}/dbus-1/interfaces/org.kde.FavIcon.xml
%{_kf5_datadir}/templates/*.desktop
%{_kf5_datadir}/templates/.source/*

%files devel
%{_kf5_libdir}/libKF5Konq.so
%{_kf5_libdir}/cmake/KF5Konq
# FIXME: This should be in a subfolder
%{_kf5_includedir}/*.h

%changelog
* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1.20141007git3ab1913
- Initial version
