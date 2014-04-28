%define framework kapidox
#%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140428git528f5a72%{?dist}
Summary:        KDE Frameworks 5 Tier 4 module for API documentation generation

License:        GPLv3 BSD  LGPLv3 QPLv1
URL:            http://download.kde.org/
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kapidox-528f5a72.tar


BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  python-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 4 module for API documentation generation

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kf5_prefix}/lib/python2.7/site-packages/kapidox
%{_kf5_prefix}/lib/python2.7/site-packages/kapidox-5.0.0-py2.7.egg-info
%{_kf5_bindir}/kgenapidox
%{_kf5_bindir}/depdiagram-prepare
%{_kf5_bindir}/depdiagram-generate
%{_kf5_bindir}/kgenframeworksapidox
%{_kf5_bindir}/depdiagram-generate-all

%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428git528f5a72
- Update to git: 528f5a72

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git7d7516c0
- Update to git: 7d7516c0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140206git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Siddharth Sharma <siddharths@fedoraproject.org> - 4.95.0-1
- Initial Release
