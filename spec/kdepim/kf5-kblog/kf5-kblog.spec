%global framework kblog

Name:           kf5-%{framework}
Version:        15.11.80
Release:        1%{?dist}
Summary:        The KBlog Library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/pim/%{framework}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel

BuildRequires:  kf5-kcoreaddons-devel >= 5.15
BuildRequires:  kf5-kdelibs4support-devel >= 5.15
BuildRequires:  kf5-kio-devel >= 5.15
BuildRequires:  kf5-kxmlrpcclient-devel >= 5.15

BuildRequires:  kf5-kcalendarcore-devel >= 15.11.80
BuildRequires:  kf5-syndication-devel >= 15.11.80

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
The KBlog library can retrieve, update or create blog posts on various popular
blogging platforms like Wordpress or Blogspot.com.
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-kcalendarcore-devel
Requires:       kf5-syndication-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
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
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING.LIB
%{_kf5_libdir}/libKF5Blog.so.*

%files devel
%{_kf5_includedir}/kblog_version.h
%{_kf5_includedir}/KBlog
%{_kf5_libdir}/libKF5Blog.so
%{_kf5_libdir}/cmake/KF5Blog
%{_kf5_archdatadir}/mkspecs/modules/qt_KBlog.pri


%changelog
* Thu Dec 03 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.80-1
- Update to 15.11.80

* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
