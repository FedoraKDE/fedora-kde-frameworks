
Name:    kf5-kfilemetadata
Summary: A Tier 3 KDE Framework for extracting file metadata
Version: 4.97.0
Release: 1%{?dist}

# # KDE e.V. may determine that future LGPL versions are accepted
License: LGPLv2 or LGPLv3
URL:     https://projects.kde.org/projects/kde/kdelibs/%{name}

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz
Source0: kf5-kfilemetadata-%{version}.tar
## upstream patches

BuildRequires: extra-cmake-modules
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-umbrella
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-karchive-devel
BuildRequires: qt5-qtbase-devel

BuildRequires: ebook-tools-devel
BuildRequires: pkgconfig(exiv2) >= 0.20
BuildRequires: pkgconfig(poppler-qt5)
BuildRequires: pkgconfig(taglib)

%description
%{summary}.

%package devel
Summary:  Developer files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: kf5-ki18n-devel
Requires: kf5-kservice-devel
Requires: kf5-karchive-devel

%description devel
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LGPL*
#%{_kf5_libdir}/libKF5FileMetaData.so.*
%{_kf5_libdir}/libkfilemetadata.so.*
%{_kf5_plugindir}/kfilemetadata_epubextractor.so
%{_kf5_plugindir}/kfilemetadata_exiv2extractor.so
%{_kf5_plugindir}/kfilemetadata_odfextractor.so
%{_kf5_plugindir}/kfilemetadata_office2007extractor.so
%{_kf5_plugindir}/kfilemetadata_officeextractor.so
%{_kf5_plugindir}/kfilemetadata_plaintextextractor.so
%{_kf5_plugindir}/kfilemetadata_popplerextractor.so
%{_kf5_plugindir}/kfilemetadata_taglibextractor.so
%{_kf5_datadir}/kde5/services/kfilemetadata_epubextractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_exiv2extractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_odfextractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_office2007extractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_officeextractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_plaintextextractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_popplerextractor.desktop
%{_kf5_datadir}/kde5/services/kfilemetadata_taglibextractor.desktop
%{_kf5_datadir}/kde5/servicetypes/kfilemetadataextractor.desktop

%files devel
#%{_kf5_libdir}/libKF5FileMetaData.so
%{_kf5_libdir}/libkfilemetadata.so
%{_kf5_libdir}/cmake/KF5FileMetaData
%{_kf5_includedir}/KFileMetaData

%changelog
* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1
- Fox kfilemetadata into kf5-kfilemetadata

