%define framework ktexteditor

Name:           kf5-%{framework}
Version:        4.99.0
Release:        1%{?_dist}
Summary:        KDE Frameworks 5 Tier 3 advanced embeddable text editor

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

Source0:        %{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-sonnet-devel

Requires:       kf5-filesystem

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kparts-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

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
%{_sysconfdir}/xdg/kate*
%{_kf5_libdir}/libKF5TextEditor.so.*
%{_kf5_plugindir}/katepart.so
%{_kf5_datadir}/kservices5/katepart.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/katepart5/script/
%{_kf5_datadir}/katepart5/syntax/
%{_kf5_datadir}/katepart/katepart5ui.rc

%files devel
%{_kf5_libdir}/libKF5TextEditor.so
%{_kf5_libdir}/cmake/KF5TextEditor
%{_kf5_includedir}/ktexteditor_version.h
%{_kf5_includedir}/KTextEditor
%{_kf5_archdatadir}/mkspecs/modules/qt_KTextEditor.pri


%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Fri May 02 2014 Jan Grulich <jgrulich@redhat.com> - 5.0.90-1
- initial version
