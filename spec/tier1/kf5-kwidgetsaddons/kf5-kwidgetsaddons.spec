#%define snapshot 20140205
%define framework kwidgetsaddons

Name:           kf5-%{framework}
Version:        4.98.0
Release:        1.20140428gitf8892042%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon with various classes on top of QtWidgets

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kwidgetsaddons-f8892042.tar

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 1 addon with item views


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


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
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5WidgetsAddons.so.*
%{_kf5_datadir}/kcharselect


%files devel
%{_kf5_includedir}/kwidgetsaddons_version.h
%{_kf5_includedir}/KWidgetsAddons
%{_kf5_libdir}/libKF5WidgetsAddons.so
%{_kf5_libdir}/cmake/KF5WidgetsAddons
%{_kf5_archdatadir}/mkspecs/modules/qt_KWidgetsAddons.pri


%changelog
* Mon Apr 28 2014 dvratil <dvratil@redhat.com> - 4.98.0-1.20140428gitf8892042
- Update to git: f8892042

* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422git9f9c9bab
- Update to git: 9f9c9bab

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitcd653694
- Update to git: cd653694

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Tue Mar 11 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-2
- fix button box access

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
