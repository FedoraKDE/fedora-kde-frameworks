%define framework khtml
#%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.100.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 solution with KHTML, a HTML rendering engine

License:        LGPLv2+ and GPLv3
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz


BuildRequires:  fdupes
BuildRequires:  giflib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  phonon-qt5-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-sonnet-devel

Requires:       kf5-filesystem

%description
KHTML is a web rendering engine, based on the KParts technology and using KJS
for JavaScript support.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-karchive-devel
Requires:       kf5-kcodecs-devel
Requires:       kf5-kglobalaccel-devel
Requires:       kf5-ki18n-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-kio-devel
Requires:       kf5-kjs-devel
Requires:       kf5-knotifications-devel
Requires:       kf5-kparts-devel
Requires:       kf5-ktextwidgets-devel
Requires:       kf5-kwallet-devel
Requires:       kf5-kwidgetsaddons-devel
Requires:       kf5-kwindowsystem-devel
Requires:       kf5-kxmlgui-devel
Requires:       kf5-sonnet-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DCMAKE_SHARED_LINKER_FLAGS="-Wl,--as-needed"
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang khtml5_qt --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f khtml5_qt.lang
%doc COPYING.GPL3 COPYING.LIB README.md
%{_kf5_libdir}/libKF5KHtml.so.*
%{_kf5_qtplugindir}/*.so
%{_kf5_datadir}/kf5/kjava/
%{_kf5_datadir}/kf5/khtml/
%{_kf5_datadir}/khtml/
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_sysconfdir}/xdg/khtmlrc

%files devel
%doc
%{_kf5_libdir}/libKF5KHtml.so
%{_kf5_libdir}/cmake/KF5KHtml/*.cmake
%{_kf5_includedir}/KHtml/
%{_kf5_includedir}/khtml_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_KHtml.pri


%changelog
* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140206git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Thu Jan 09 2014 Siddharth Sharma <siddharths@fedoraproject.org>
- Initial Release
