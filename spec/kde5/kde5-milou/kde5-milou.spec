%define git_commit 9f6e0ce
%define base_name milou

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140515git%{git_commit}%{?_dist}
Summary:        A dedicated KDE search application built on top of Baloo

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-baloo-devel

Requires:       kde5-filesystem

Conflicts:      milou < 4.96.0
Provides:       milou = %{version}-%{release}

%description
%{summary}.

%prep
%setup -q -n %{base_name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_datadir}/kservicetypes5/miloupreviewplugin.desktop
%{_kde5_libdir}/libmilou.so
%{_kde5_libdir}/qml/org/kde/milou
%{_kde5_datadir}/plasma/plasmoids/org.kde.milou
%{_datadir}/kservices5/plasma-applet-org.kde.milou.desktop


%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515gitc11b832c
- Intial snapshot
