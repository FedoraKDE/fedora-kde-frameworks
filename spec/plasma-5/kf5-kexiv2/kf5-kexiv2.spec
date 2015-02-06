%global framework   kexiv2
%global git_date    20150127
%global git_commit  5e982dd

Name:           kf5-%{framework}
Summary:        An Exiv2 wrapper library
Version:        5.0.0
Release:        1.%{git_date}git%{git_commit}%{?dist}

# # KDE e.V. may determine that future LGPL versions are accepted
License:        GPLv2+ and LGPLv2+
URL:            https://www.kde.org

#%global revision %(echo %{version} | cut -d. -f3)
#%if %{revision} >= 50
#%global stable unstable
#%else
#%global stable stable
#%endif
#Source0:        http://download.kde.org/%{stable}/plasma/%{plasma_version}/%{framework}-%{version}.tar.xz

# git archive --format=tar.gz --remote=git://anongit.kde.org/libkexiv2.git \
#             --prefix=libkexiv2-%{version}/ --output=libkexiv2-%{git_commit}.tar.gz \
#             frameworks
Source0:        libkexiv2-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ktextwidgets-devel

BuildRequires:  exiv2-devel >= 0.24

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ki18n-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-ktextwidgets-devel

%description devel
%{summary}.


%prep
%setup -q -n libkexiv2-%{version}


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
%doc COPYING COPYING.LIB
%{_kf5_libdir}/libKF5KExiv2.so.*
%{_datadir}/libkexiv2

%files devel
%{_kf5_libdir}/libKF5KExiv2.so
%{_kf5_libdir}/cmake/KF5KExiv2
%{_kf5_includedir}/KExiv2
%{_kf5_includedir}/libkexiv2_version.h

%changelog
* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1.20150127git5e982dd
- Initial git snapshot
