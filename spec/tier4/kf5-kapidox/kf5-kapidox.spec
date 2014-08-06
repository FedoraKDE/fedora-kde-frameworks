%define framework kapidox
#%define snapshot 20140206

Name:           kf5-%{framework}
Version:        5.1.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 scripts and data for building API documentation
BuildArch:      noarch

License:        BSD
URL:            http://download.kde.org/
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/stable/frameworks/%{version}/%{framework}-%{version}.tar.xz


BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  python2-devel

Requires:       kf5-filesystem

%description
Scripts and data for building API documentation (dox) in a standard format and
style.

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
%doc LICENSE
%{python2_sitelib}/kapidox
%{python2_sitelib}/kapidox-5.0.0-py2.7.egg-info
%{_kf5_bindir}/kgenapidox
%{_kf5_bindir}/depdiagram-prepare
%{_kf5_bindir}/depdiagram-generate
%{_kf5_bindir}/kgenframeworksapidox
%{_kf5_bindir}/depdiagram-generate-all

%changelog
* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Mon Jul 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-2
- Fixed License
- Fixed summary
- Fixed BR
- Made package noarch
- Added license

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

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
