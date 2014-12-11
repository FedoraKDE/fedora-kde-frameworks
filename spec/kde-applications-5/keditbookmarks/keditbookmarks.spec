%global git_date    20141024
%global git_commit  8a1c3ad

Name:           keditbookmarks
Version:        4.97.0
Release:        2.%{git_date}git%{git_commit}%{?dist}
Summary:        Bookmark organizer and editor

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar.gz --remote=git://anongit.kde.org/kde-baseapps.git \
#             --output=kde-baseapps-%%{git_commit}.tar.gz \
#             --prefix=kde-baseapps-%%{version}/ %%{git_commit}
Source0:        kde-baseapps-%{git_commit}.tar.gz

Patch0:         keditbookmarks-standalone-build.patch

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kdelibs4support-devel

# Unstable
BuildRequires:  kf5-konq-devel

Requires:       kf5-filesystem
Requires:       kio-extras

%description
%{summary}.

%package        libs
Summary:        KEditBookmarks runtime libraries
%description    libs
%{summary}.


%prep
%setup -q -n kde-baseapps-%{version}

%patch0 -p1 -b .build

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ../keditbookmarks
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

rm %{buildroot}/%{_libdir}/libkbookmarkmodel_private.so

%files
%doc COPYING COPYING.DOC COPYING.LIB
%{_bindir}/kbookmarkmerger
%{_bindir}/keditbookmarks
%{_libdir}/libkdeinit5_keditbookmarks.so
%{_datadir}/config.kcfg/keditbookmarks.kcfg
%{_kf5_datadir}/kxmlgui5/keditbookmarks
%{_datadir}/applications/org.kde.keditbookmarks.desktop


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/libkbookmarkmodel_private.so.*

%changelog
* Sat Oct 25 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-ě.20141024git8a1c3ad
- split -libs

* Fri Oct 24 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-1.20141024git8a1c3ad
- Initial version
