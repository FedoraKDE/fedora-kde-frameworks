%define         framework baloo-widgets
%define         git_commit 2dd6cb9
%define         git_date 20141024

Name:           kf5-%{framework}
Version:        5.0.0
Release:        1.%{git_date}git%{git_commit}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 module that provides widgets built on top of Baloo

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
# git archive --format=tar.gz --remote=git://anongit.kde.org/%%{framework}.git \
#             --prefix=%%{framework}-%%{version}/ --output=%%{framework}-%%{git_commit}.tar.gz \
#              master
Source0:        %{framework}-%{git_commit}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kfilemetadata-devel
BuildRequires:  kf5-baloo-devel
BuildRequires:  kf5-kdelibs4support-devel

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5BalooWidgets.so.*
%{_kf5_bindir}/baloo_filemetadata_temp_extractor

%files devel
%{_kf5_libdir}/libKF5BalooWidgets.so
%{_kf5_libdir}/cmake/KF5BalooWidgets
%{_kf5_includedir}/BalooWidgets

%changelog
* Fri Oct 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1.20141024git2dd6cb9
- Initial version (git snapshot)
