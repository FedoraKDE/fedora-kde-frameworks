%global git_date 20150122
%global git_commit b57e062

%global framework kpeople

Name:           kf5-%{framework}
Version:        0.5.60
Release:        1.%{git_date}git%{git_commit}%{?dist}
License:        GPLv2+
URL:            https://projects.kde.org/projects/playground/network/libkpeople
Summary:        Meta-contact aggregation library


# git archive --format=tar.gz --remote=git://anongit.kde.org/libkpeople.git --prefix=libkpeople-%%{version} /
#             --output=libkpeople-%%{git_commit}.tar.gz master
Source0:        libkpeople-%{git_commit}.tar.gz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kitemviews-devel

BuildRequires:  kf5-baloo-devel

Requires:       kf5-filesystem

%description
A library that provides access to all contacts and the people who hold them.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libkpeople-%{version}

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
%doc COPYING
%{_kf5_libdir}/libKPeople.so.*
%{_kf5_libdir}/libKPeopleWidgets.so.*
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_qmldir}/org/kde/people
%{_kf5_datadir}/kpeople

%files devel
%{_kf5_libdir}/libKPeople.so
%{_kf5_libdir}/libKPeopleWidgets.so
%{_kf5_includedir}/KPeople
%{_kf5_libdir}/cmake/KF5People


%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.5.60-1.20150122gitb57e062
- Update to latest git

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.5.0-1.20150122git88f8e64
- Fork from libkpeople
