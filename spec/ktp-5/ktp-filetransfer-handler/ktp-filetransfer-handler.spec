%global         git_date    20150122
%global         git_commit  a475a4b

Name:           ktp-filetransfer-handler
Summary:        Telepathy file transfer handler
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

BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kconfig-devel

BuildRequires:  ktp-common-internals-devel >= %{version}


Obsoletes:      telepathy-kde-filetransfer-handler < 0.3.0
Provides:       telepathy-kde-filetransfer-handler = %{version}-%{release}

%description
Telepathy-KDE file transfer handler. It basically does two thigs:
 - Send files to your contact
 - Receive files from your contact

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
%doc COPYING AUTHORS NEWS README TODO
%{_libexecdir}/ktp-filetransfer-handler
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.KTp.FileTransferHandler.service
%{_datadir}/telepathy/clients/KTp.FileTransferHandler.client


%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 0.9.60-1.20150122gita475a4b
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
- 0.5.80

* Sun Feb 17 2013 Jan Grulich <jgrulich@redhat.com> - 0.5.3-1
- 0.5.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Jan Grulich <jgrulich@redhat.com> - 0.5.2-1
- 0.5.2

* Fri Oct 05 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.5.1-1
- 0.5.1

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> 0.5.0-1
- 0.5.0

* Thu Jul 26 2012 Jan Grulich <jgrulich@redhat.com> - 0.4.1-1
- 0.4.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.0-1
- 0.4.0

* Mon Apr 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.1-1
- 0.3.1

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-3
- update %%description

* Thu Feb 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- drop BR: desktop-file-utils telepathy-qt4-devel
- %%doc AUTHORS NEWS README TODO

* Tue Jan 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- ktp-filetransfer-handler-0.3.0

* Fri Nov 25 2011 Rex Dieter <rdieter@fedoraproject.org> 0.2.0-1
- 0.2.0

* Thu Sep 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-2
- fix Source0 URL
- fix tabs/spaces

* Fri Aug 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.1.0-1
- first try

