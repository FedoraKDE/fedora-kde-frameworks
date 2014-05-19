%define git_commit 60d6c72
%define base_name kde-cli-tools

Name:           kde5-cli-tools
Version:        4.96.0
Release:        1.20140519git%{git_commit}%{?dist}
Summary:        Tools based on KDE Frameworks 5 to better interact with the system.

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
# Source0:        http://download.kde.org/unstable/kde-baseapps/%{version}/kde-baseapps-%{version}.tar.xz
Source0:        %{base_name}-%{git_commit}.tar.xz

Patch0:         kde-cli-tools-fix-build.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kde5-rpm-macros

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdelibs4support-devel

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

%patch0 -R -p1 -b .fixbuild

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}


%files
%{_kde5_bindir}/kcmshell5
%{_kde5_bindir}/kde-open5
%{_kde5_bindir}/kdecp5
%{_kde5_bindir}/kdemv5
%{_kde5_bindir}/keditfiletype5
%{_kde5_bindir}/kioclient5
%{_kde5_bindir}/kmimetypefinder5
%{_kde5_bindir}/kstart5
%{_kde5_bindir}/ksvgtopng5
%{_kde5_bindir}/ktraderclient5
%{_kde5_libdir}/libkdeinit5_kcmshell5.so
%{_kde5_plugindir}/kcm_filetypes.so
%{_kde5_libexecdir}/kdeeject
%{_kde5_libexecdir}/kdesu
%{_datadir}/doc/HTML/en/kdesu
%{_datadir}/kservices5/filetypes.desktop
%{_datadir}/man/man1/kdesu.1.gz

%changelog
* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140519git60d6c72
- initial version
