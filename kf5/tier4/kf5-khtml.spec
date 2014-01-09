%define snapshot git010814171303
Name:           kf5-khtml
Version:        5.0.0
Release:        0.1.%{snapshot}%{?dist}
Summary:        KDE Core Libraries

License:        GPLv3 
URL:            http://www.kde.org
#kf5-khtml-git010814171303.tar.bz2
Source0:        %{name}-%{snapshot}.tar.bz2

BuildRequires:  attica-qt5-devel >= 1.0.0
BuildRequires:  cmake >= 2.8.12
BuildRequires:  extra-cmake-modules >= 0.0.9
BuildRequires:  fdupes
BuildRequires:  giflib-devel
BuildRequires:  kf5-filesystem
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  libjpeg-devel
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  libpng-devel
BuildRequires:  phonon-qt5-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  zlib-devel

%description
Kf5-kthml contains the core libraries of K Desktop Environment
It is mandatory package for KDE Applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{snapshot}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DCMAKE_SHARED_LINKER_FLAGS="-Wl,--as-needed"
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING.GPL3 COPYING.LIB README.md
%{_kf5_libdir}/*.so.*
%{_kf5_libdir}/plugins/kf5/*.so
%{_kf5_datadir}/kjava/
%{_kf5_datadir}/khtml/
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_sysconfdir}/xdg/khtmlrc

%files devel
%doc
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5KHtml/*.cmake
%{_kf5_includedir}/KHtml/
%{_kf5_includedir}/*.h
%{_kf5_datadir}/dbus-1/interfaces/org.kde.KHtmlPart.xml

%changelog

* Thu Jan 09 2014 Siddharth Sharma <siddharths@fedoraproject.org> - kf5-html- 5.0.0-0.1.git010814171303
- Initial Release
 
