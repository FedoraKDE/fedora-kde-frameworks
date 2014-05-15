#%define snapshot 20140205

# libksysguard
%define framework ksysguard
%define git_commit f7a2bbe

Name:           kf5-%{framework}
Version:        4.96.0
Release:        1.20140514git%{git_commit}%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon for process management

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2

#Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz
Source0:        %{framework}-%{git_commit}.tar.xz

BuildRequires:  zlib-devel
BuildRequires:  libXres-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtwebkit-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kconfig-devel

Requires:       kf5-filesystem

%description
KSysGuard library provides API to read and manage processes running on the system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

# FIXME: Until ksysguard is correctly frameworkized, it conflicts with kde-workspace-devel
Conflicts:      kde-workspace-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DINCLUDE_INSTALL_DIR=%{_kf5_includedir}
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB
%{_kf5_libdir}/liblsofui.so.*
%{_kf5_libdir}/libprocessui.so.*
%{_kf5_libdir}/libprocesscore.so.*
%{_kf5_libdir}/libksignalplotter.so.*
%{_kf5_libdir}/libksgrd.so.*
%{_kf5_datadir}/ksysguard

%files devel
%{_kf5_includedir}/ksysguard
%{_kf5_libdir}/liblsofui.so
%{_kf5_libdir}/libprocessui.so
%{_kf5_libdir}/libprocesscore.so
%{_kf5_libdir}/libksignalplotter.so
%{_kf5_libdir}/libksgrd.so
%{_kf5_libdir}/cmake/KF5SysGuard

%changelog
* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140514gitf7a2bbe
- Update to latest git snapshot

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1.20140425git1908ec8
- Initial package
