%define git_commit 4f5f60b
%define base_name kate

Name:           kde5-%{base_name}
Version:        4.90.1
Release:        1.20140524git%{git_commit}%{?_dist}
Summary:        Advanced KDE editor applications

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        %{base_name}-%{git_commit}.tar.xz

Patch0:         kate-fix-build.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kde5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-umbrella
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kinit-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-ktexteditor-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel

Requires:       kde5-filesystem

Conflicts:      kde-runtime
Conflicts:      kwrite
Conflicts:      kate
Provides:       kate = %{version}-%{release}
Provides:       kwrite = %{version}-%{release}

%description
An advanced editor component which is used in numerous KDE applications
requiring a text editing component.

%prep
%setup -q -n %{base_name}-%{version}

%patch0 -p1 -b .build

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
%doc AUTHORS COPYING-GPL3 COPYING-LGPL3 COPYING.LIB README.md
%{_kde5_bindir}/kwrite
%{_kde5_bindir}/kate
%{_kde5_libdir}/libkdeinit5_kate.so
%{_kde5_libdir}/libkdeinit5_kwrite.so
%{_kde5_plugindir}/*.so
%{_kde5_sysconfdir}/xdg/katerc
%{_kde5_datadir}/kate/kateui.rc
%{_kde5_datadir}/kwrite/kwriteui.rc
%{_kde5_datadir}/katefiletree
%{_kde5_datadir}/katesearch
%{_kde5_datadir}/kateproject
%{_kde5_datadir}/katekonsole
%{_kde5_datadir}/katectags
%{_kde5_datadir}/katesql
%{_kde5_datadir}/katexmltools
%{_kde5_datadir}/kateopenheaderplugin
%{_kde5_datadir}/katecloseexceptplugin
%{_kde5_datadir}/kategdb
%{_kde5_datadir}/katebuild
%{_datadir}/icons/hicolor/*/actions/*
%{_datadir}/applications/org.kate-editor.kwrite.desktop
%{_datadir}/applications/org.kde.kate.desktop
%{_datadir}/kservices5/*.desktop
%{_datadir}/doc/HTML/en/kate
%{_datadir}/doc/HTML/en/katepart
%{_datadir}/man/man1/kate.1.gz


%changelog
* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git4f5f60b
- Intial snapshot
