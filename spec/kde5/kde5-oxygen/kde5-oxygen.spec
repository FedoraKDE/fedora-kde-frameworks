%define git_commit 9651288
%define base_name oxygen

Name:           kde5-%{base_name}
Version:        4.96.0
Release:        1.20140515git%{git_commit}%{?_dist}
Summary:        KDE's default style and look

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kde5-filesystem

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

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
%doc COPYING
%{_kde5_bindir}/oxygen-demo5
%{_kde5_bindir}/oxygen-settings5
%{_kde5_bindir}/oxygen-shadow-demo5
%{_kde5_libdir}/*.so.*
%{_kde5_plugindir}/kstyle_oxygen_config.so
%{_kde5_plugindir}/kwin/kdecorations/config/kwin_oxygen_config.so
%{_kde5_plugindir}/kwin/kdecorations/kwin3_oxygen.so
%{_kde5_plugindir}/styles/oxygen.so
%{_kde5_datadir}/kstyle/themes/oxygen.themerc
%{_datadir}/icons/*
%{_datadir}/sounds/*


%files devel
%{_kde5_libdir}/*.so

%changelog
* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140515git9651288
- Intial snapshot
