%define framework khtml
#%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140428git18dc6c63%{?dist}
Summary:        KDE Frameworks 5 Tier 4 solution with KHTML engine

License:        GPLv3
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-khtml-18dc6c63.tar


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

BuildRequires:  kf5-attica-devel
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

Requires:       kf5-filesystem

%description
KHTML is a web rendering engine, based on the KParts technology and using KJS
for JavaScript support.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING.GPL3 COPYING.LIB README.md
%{_kf5_libdir}/libKF5KHtml.so.*
%{_kf5_qtplugindir}/kf5/*.so
%{_kf5_datadir}/kjava/
%{_kf5_datadir}/khtml/
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_sysconfdir}/xdg/khtmlrc

%files devel
%doc
%{_kf5_libdir}/libKF5KHtml.so
%{_kf5_libdir}/cmake/KF5KHtml/*.cmake
%{_kf5_includedir}/KHtml/
%{_kf5_includedir}/khtml_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_KHtml.pri


%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git18dc6c63
- Update to git: 18dc6c63

* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git76a35101
- Update to git: 76a35101

* Thu Apr 24 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140424gitd83334e3
- Update to git: d83334e3

* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git387c3324
- Update to git: 387c3324

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitc6d7b4ab
- Update to git: c6d7b4ab

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
