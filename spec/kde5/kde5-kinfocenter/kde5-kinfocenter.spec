%define git_commit b9f69a0
%define base_name kinfocenter

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140524git%{git_commit}%{?dist}
Summary:        KDE Info Center

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel

BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libX11-devel
BuildRequires:  pciutils-devel
BuildRequires:  libraw1394-devel

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Provides:       kinfocenter = %{version}-%{release}

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
%doc COPYING COPYING.DOC
%{_kde5_bindir}/kinfocenter
%{_kde5_plugindir}/*.so
%{_kde5_datadir}/kinfocenter
%{_kde5_datadir}/kcmview1394
%{_kde5_datadir}/kcmusb
%{_kde5_sysconfdir}/xdg/menus/kde-information.menu
%{_datadir}/applications/kinfocenter.desktop
%{_datadir}/doc/HTML/en/kinfocenter
%{_datadir}/kservices5/*.desktop
%{_datadir}/kservicetypes5/*.desktop
%{_datadir}/desktop-directories/kde-information.directory


%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git1b86b1a
- Intial snapshot
