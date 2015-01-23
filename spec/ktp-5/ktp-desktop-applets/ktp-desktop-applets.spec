%global         git_date    20150122
%global         git_commit  14742ef

Name:           ktp-desktop-applets
Summary:        KDE Telepathy desktop applets
Version:        0.9.60
Release:        1.%{git_date}git%{git_commit}%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/extragear/network/telepathy/%{name}
#Source0:        http://download.kde.org/stable/kde-telepathy/%{version}/src/%{name}-%{version}.tar.bz2

# git archive --format=tar.gz --remote=git://anongit.kde.org/%%{name}.git \
#             --prefix=%%{name}-%%{version}/ --output=%%{name}-%%{git_commit}.tar.gz %%{git_commit}
Source0:        %{name}-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-plasma-devel


Obsoletes:      telepathy-kde-presence-applet < 0.3.0
Provides:       telepathy-kde-presence-applet = %{version}-%{release}

# not sure where best to put this other than here -- rex
Obsoletes:      telepathy-kde-presence-dataengine < 0.3.0
Provides:       telepathy-kde-presence-dataengine = %{version}-%{release}

Obsoletes:      ktp-contact-applet < 0.5.80
Obsoletes:      ktp-presence-applet < 0.5.80
Provides:       ktp-contact-applet = %{version}-%{release}
Provides:       ktp-presence-applet = %{version}-%{release}

Requires:       kf5-plasma

%description
KDE Telepathy desktop applets, including:
* contacts
* presence

%prep
%setup -q -n %{name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%files
%doc COPYING
%{_kf5_datadir}/plasma/plasmoids/org.kde.person
%{_kf5_datadir}/plasma/plasmoids/org.kde.ktp-chat
%{_kf5_datadir}/plasma/plasmoids/org.kde.ktp-contactlist
%{_kf5_datadir}/kservices5/*.desktop


%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.60-1.20150122git14742ef
- Update to experimental KF5 version

* Mon Oct 20 2014 Jan Grulich <jgrulich@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed Sep 17 2014 Jan Grulich <jgrulich@redhat.com> - 0.8.80-1
- Update to 0.8.80 (beta)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Jan Grulich <jgrulich@redhat.com> 0.8.1-1
- 0.8.1

* Wed Mar 12 2014 Jan  Grulich <jgrulich@redhat.com> 0.8.0-1
- 0.8.0

* Wed Feb 26 2014 Jan Grulich <jgrulich@redhat.com> - 0.7.80-1
- 0.7.80

* Wed Jan 15 2014 Jan Grulich <jgrulich@redhat.com> 0.7.1-1
- 0.7.1

* Tue Oct 29 2013 Jan Grulich <jgrulich@redhat.com> - 0.7.0-1
- 0.7.0

* Wed Sep 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.80-1
- 0.6.80

* Tue Aug 06 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-1
- 0.6.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Jan Grulich <jgrulich@redhat.com> 0.6.2-1
- 0.6.2

* Wed Apr 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.1-1
- 0.6.1

* Tue Apr 02 2013 Jan Grulich <jgrulich@redhat.com> - 0.6.0-1
- 0.6.0

* Thu Mar 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.5.80-1
- ktp-desktop-applets-0.5.80

