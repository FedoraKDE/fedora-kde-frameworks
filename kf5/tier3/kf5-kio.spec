%define snapshot 20140205
%define framework kio

Name:           kf5-%{framework}
Version:        4.96.0
Release:        0.1.%{snapshot}git%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for filesystem abstraction

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  zlib-devel

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kglobalaccel-devel

%description
KDE Frameworks 5 Tier 3 solution for filesystem abstraction


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    doc
Documentation for %{name}.

# TODO: Split the package

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_libdir}/*.so.*
%{_kf5_bindir}/*
%{_kf5_sysconfdir}/xdg/accept-languages.codes
%{_kf5_plugindir}/*.so
%{_kf5_libexecdir}/*
%{_kf5_datadir}/applications/kde5/*.desktop
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/kconf_update/*
%{_kf5_datadir}/kde5/services/*
%{_kf5_datadir}/kde5/servicetypes/*
%{_kf5_datadir}/proxyscout/
%{_kf5_datadir}/khtml/domain_info

%files devel
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5KIO
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOFileWidgets.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KNTLM.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOWidgets.pri

%files doc
%{_kf5_mandir}/man8/*
%{_kf5_datadir}/doc/HTML/en/kioslave/


%changelog
* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Mon Jan 20 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rebuild against new kf5-filesystem

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

