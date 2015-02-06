%global framework   kipi-plugins
%global git_date    20150127
%global git_commit  cb19055

Name:           kf5-%{framework}
Summary:        Plugins to use with kf5-kipi
Version:        5.0.0
Release:        1.%{git_date}git%{git_commit}%{?dist}

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

# git archive --format=tar.gz --remote=git://anongit.kde.org/kipi-plugins.git \
#             --prefix=kipi-plugins-%{version}/ --output=kipi-plugins-%{git_commit}.tar.gz \
#             frameworks
Source0:        %{framework}-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtxmlpatterns-devel

BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kdelibs4support-devel

BuildRequires:  kf5-kdcraw-devel
BuildRequires:  kf5-kexiv2-devel
BuildRequires:  kf5-kipi-devel

BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libjpeg-turbo-devel

BuildRequires:  desktop-file-utils

Requires:       kf5-kipi

%description
%{summary}.

%prep
%setup -q -n %{framework}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# no -devel
rm %{buildroot}/%{_kf5_libdir}/libKF5kipiplugins.so

%check
desktop-file-validate %{buildroot}/%{_kf5_datadir}/applications/kipiplugins.desktop

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
%doc COPYING COPYING-ADOBE README
%{_kf5_libdir}/libKF5kipiplugins.so.*
%{_kf5_datadir}/kservices5/kipiplugin_*.desktop
%{_kf5_qtplugindir}/kipiplugin_*.so
%{_kf5_datadir}/kxmlgui5/kipi/kipiplugin_*.rc
%{_kf5_datadir}/kipiplugin_printimages
%{_kf5_datadir}/kipiplugin_flashexport
%{_kf5_datadir}/kipi/tips
%{_kf5_datadir}/applications/kipiplugins.desktop
%{_datadir}/icons/hicolor/*/*/*.png


%changelog
* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1.20150127gitcb19055
- Initial git snapshot
