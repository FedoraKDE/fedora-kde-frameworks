Name:    kde5-baloo
Summary: A framework for searching and managing metadata
Version: 4.90.0
Release: 1%{?dist}

License: GPLv2 and LGPLv2
URL:     https://projects.kde.org/projects/kde/kdelibs/baloo

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git frameworks | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

## upstream patches

BuildRequires: doxygen
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: kfilemetadata-devel >= %{version}
BuildRequires: pkgconfig(akonadi) >= 1.11.80
BuildRequires: pkgconfig(QJson)
# for %%{_polkit_qt_policydir} macro
BuildRequires: polkit-qt-devel
BuildRequires: xapian-core-devel

# kio_tags/kio_timeline moved here from kde-runtime
Conflicts: kde-runtime < 4.12.90

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4%{?_isa}%{?_kde4_version: >= %{_kde4_version}}

%description
%{summary}.

%package devel
Summary:  Developer files for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.

%package libs
Summary:  Runtime libraries for %{name}
Requires: kdelibs4%{?_isa} >= %{version}
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files
%doc COPYING COPYING.LIB
%{_sysconfdir}/dbus-1/system.d/org.kde.baloo.filewatch.conf
%{_kde4_bindir}/akonadi_baloo_indexer
%{_kde4_bindir}/baloo_file
%{_kde4_bindir}/baloo_file_cleaner
%{_kde4_bindir}/baloo_file_extractor
%{_kde4_bindir}/baloosearch
%{_kde4_bindir}/balooshow
%{_kde4_libexecdir}/kde_baloo_filewatch_raiselimit
%{_kde4_datadir}/akonadi/agents/akonadibalooindexingagent.desktop
%{_kde4_datadir}/autostart/baloo_file.desktop
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_datadir}/dbus-1/system-services/org.kde.baloo.filewatch.service
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_datadir}/kde4/services/baloo_contactsearchstore.desktop
%{_kde4_datadir}/kde4/services/baloo_emailsearchstore.desktop
%{_kde4_datadir}/kde4/services/baloo_filesearchstore.desktop
%{_kde4_datadir}/kde4/services/baloo_notesearchstore.desktop
%{_kde4_datadir}/kde4/services/baloosearch.protocol
%{_kde4_datadir}/kde4/services/kcm_baloofile.desktop
%{_kde4_datadir}/kde4/services/plasma-runner-baloosearch.desktop
%{_kde4_datadir}/kde4/services/tags.protocol
%{_kde4_datadir}/kde4/services/timeline.protocol
%{_kde4_datadir}/kde4/servicetypes/baloosearchstore.desktop
%{_polkit_qt_policydir}/org.kde.baloo.filewatch.policy
%{_kde4_libdir}/kde4/akonadi/akonadi_baloo_searchplugin.so
%{_kde4_libdir}/kde4/akonadi/akonadibaloosearchplugin.desktop
%{_kde4_libdir}/kde4/baloo_contactsearchstore.so
%{_kde4_libdir}/kde4/baloo_emailsearchstore.so
%{_kde4_libdir}/kde4/baloo_filesearchstore.so
%{_kde4_libdir}/kde4/baloo_notesearchstore.so
%{_kde4_libdir}/kde4/kcm_baloofile.so
%{_kde4_libdir}/kde4/kio_baloosearch.so
%{_kde4_libdir}/kde4/kio_tags.so
%{_kde4_libdir}/kde4/kio_timeline.so
%{_kde4_libdir}/kde4/krunner_baloosearchrunner.so

%files devel
%{_kde4_includedir}/baloo/
%{_kde4_libdir}/libbaloocore.so
%{_kde4_libdir}/libbaloofiles.so
%{_kde4_libdir}/libbaloopim.so
%{_kde4_libdir}/libbalooxapian.so
%{_kde4_libdir}/cmake/Baloo/

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kde4_libdir}/libbaloocore.so.4*
%{_kde4_libdir}/libbaloofiles.so.4*
%{_kde4_libdir}/libbaloopim.so.4*
%{_kde4_libdir}/libbalooxapian.so.4*



%changelog
* Tue Apr 15 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.0-2
- respin

* Sat Apr 12 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.0-1
- 4.13.0

* Thu Apr 03 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.97-1
- 4.12.97

* Sat Mar 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.95-1
- 4.12.95

* Mon Mar 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.12.90-1
- baloo-4.12.90, first try

