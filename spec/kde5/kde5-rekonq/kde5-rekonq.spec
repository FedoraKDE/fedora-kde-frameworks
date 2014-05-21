%define git_commit cdf27f0
%define base_name rekonq

Name:           kde5-%{base_name}
Version:        2.90.0
Release:        1.20140521git%{git_commit}%{?dist}
Summary:        A web browser for KDE based on WebKit

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/kde-workspace.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/plasma/%{version}/kde-workspace-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qtwebkit-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel

BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kdewebkit-devel

Requires:       kde5-filesystem

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
%{_kde5_bindir}/rekonq
%{_kde5_libdir}/libkdeinit5_rekonq.so
%{_kde5_datadir}/rekonq
%{_datadir}/config.kcfg/rekonq.kcfg
%{_datadir}/applications/rekonq.desktop
%{_datadir}/icons/*/*/*/*.png

%changelog
* Wed May 21 2014 Daniel Vrátil <dvratil@redhat.com> - 2.90.0-1.20140425gitcdf27f0
- Initial version of kde5-plasma-workspace

