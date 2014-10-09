%define framework kfilemetadata

# Enable to build ffmpeg extractor
%global ffmpeg  0

Name:           kf5-%{framework}
Summary:        A Tier 3 KDE Framework for extracting file metadata
Version:        5.1.0
Release:        1%{?dist}

# # KDE e.V. may determine that future LGPL versions are accepted
License:        LGPLv2 or LGPLv3
URL:            https://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  qt5-qtbase-devel

BuildRequires:  ebook-tools-devel
BuildRequires:  pkgconfig(exiv2) >= 0.20
BuildRequires:  pkgconfig(poppler-qt5)
BuildRequires:  pkgconfig(taglib)
%if 0%{?ffmpeg}
BuildRequires:  ffmpeg-devel
%endif

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ki18n-devel
Requires:       kf5-kservice-devel
Requires:       kf5-karchive-devel

%description devel
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LGPL*
%{_kf5_libdir}/libKF5FileMetaData.so.*
%{_kf5_qtplugindir}/kfilemetadata_epubextractor.so
%{_kf5_qtplugindir}/kfilemetadata_exiv2extractor.so
%{_kf5_qtplugindir}/kfilemetadata_odfextractor.so
%{_kf5_qtplugindir}/kfilemetadata_office2007extractor.so
%{_kf5_qtplugindir}/kfilemetadata_officeextractor.so
%{_kf5_qtplugindir}/kfilemetadata_plaintextextractor.so
%{_kf5_qtplugindir}/kfilemetadata_popplerextractor.so
%{_kf5_qtplugindir}/kfilemetadata_taglibextractor.so
%{_kf5_datadir}/kservices5/kfilemetadata_epubextractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_exiv2extractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_odfextractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_office2007extractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_officeextractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_plaintextextractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_popplerextractor.desktop
%{_kf5_datadir}/kservices5/kfilemetadata_taglibextractor.desktop
%{_kf5_datadir}/kservicetypes5/kfilemetadataextractor.desktop

%if 0%{?ffmpeg}
%{_kf5_qtplugindir}/kfilemetadata_ffmpegextractor.so
%{_kf5_datadir}/kservices5/kfilemetadata_ffmpegextractor.desktop
%endif

%files devel
%{_kf5_libdir}/libKF5FileMetaData.so
%{_kf5_libdir}/cmake/KF5FileMetaData
%{_kf5_includedir}/KFileMetaData

%changelog
* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-3.20140611git034abaa
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-2.20140611gitdcc52ae
- Updated to latest git snapshot

* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1
- Fork kfilemetadata into kf5-kfilemetadata

