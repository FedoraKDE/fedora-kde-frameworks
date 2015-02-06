%global framework   kipi
%global git_date    20150127
%global git_commit  8b71323

Name:           kf5-%{framework}
Summary:        Common plugin infrastructure for KDE image applications
Version:        5.0.0
Release:        2.%{git_date}git%{git_commit}%{?dist}

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

# git archive --format=tar.gz --remote=git://anongit.kde.org/libkipi.git \
#             --prefix=libkipi-%{version}/ --output=libkipi-%{git_commit}.tar.gz \
#             frameworks
Source0:        libkipi-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kio-devel

%description
%{summary}.

%package        devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ki18n-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kparts-devel

%description    devel
%{summary}.

%prep
%setup -q -n libkipi-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc COPYING COPYING.LIB
%{_kf5_libdir}/libKF5Kipi.so.*
%{_kf5_datadir}/kservicetypes5/kipiplugin.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/kipi

%files devel
%{_kf5_libdir}/libKF5Kipi.so
%{_kf5_libdir}/cmake/KF5Kipi
%{_kf5_includedir}/KIPI
%{_kf5_includedir}/libkipi_version.h

%changelog
* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2.20150127git8b71323
- Fix -devel Requires

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1.20150127git8b71323
- Initial git snapshot
