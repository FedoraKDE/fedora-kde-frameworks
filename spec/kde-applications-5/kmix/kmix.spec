%global git_version 8c7d33c

Name:           kmix
Summary:        KDE volume control
Version:        5.0.92
Release:        20141023git%{git_version}%{?dist}

License:        GPLv2+ and GFDL
URL:            https://projects.kde.org/projects/kde/kdemultimedia/kmix

# git archive --format=tar.gz --remote=git://anongit.kde.org/kmix.git \
#             --prefix=kmix-%{version}/ --output=kmix-%{git_version}.tar.gz \
#             %{git_version}

Source0:        kmix-%{git_version}.tar.gz

# when split occured
Obsoletes:      kdemultimedia-kmix < 6:4.8.80
Provides:       kdemultimedia-kmix = 6:%{version}-%{release}

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kiconthemes-devel

BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libcanberra-devel

%description
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DKMIX_KF5_BUILD=TRUE
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%files
%doc COPYING COPYING.DOC COPYING.LIB AUTHORS
%{_libdir}/libkdeinit5_kmix.so
%{_bindir}/kmix
%{_kf5_qtplugindir}/libkded_kmixd.so
%{_kf5_datadir}/kservices5/kded/kmixd.desktop
%{_libdir}/libkdeinit5_kmixctrl.so
%{_bindir}/kmixctrl
%{_datadir}/applications/kmix.desktop
%{_bindir}/kmixremote
%{_sysconfdir}/xdg/autostart/restore_kmix_volumes.desktop
%{_sysconfdir}/xdg/autostart/kmix_autostart.desktop
%{_datadir}/kmix
%{_kf5_datadir}/kservices5/kmixctrl_restore.desktop
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/icons/hicolor/*/*/*.png

%changelog
* Thu Oct 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-20141023git8c7d33c
- KF5 version
