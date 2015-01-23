%global git_date 20150122
%global git_commit 5f2705f

Name:           kaccounts-providers
Version:        1.0
Release:        2.%{git_date}git%{git_commit}%{?dist}
Summary:        Additional service providers for KAccounts framework
License:        LGPLv2
URL:            https://projects.kde.org/projects/kdereview/kaccounts-providers
BuildArch:      noarch

# git archive --format=tar.gz --remote=git://anongit.kde.org/kaccounts-providers.git \
#             --prefix=kaccounts-providers-%%{version}/ --output=kaccounts-providers-%%{git_commit}.tar.gz \
#             %%{git_commit}

Source0:        kaccounts-providers-%{git_commit}.tar.gz

BuildRequires:  extra-cmake-modules

BuildRequires:  intltool
BuildRequires:  libaccounts-glib-devel

%description
%{summary}.

%prep
%setup -q -n kaccounts-providers-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
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
%doc COPYING
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/accounts/services/*.service
%{_datadir}/accounts/providers/*.provider
%{_sysconfdir}/signon-ui/webkit-options.d

%changelog
* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-2.20150122git0c2e1aa
- add icon scriptlets

* Thu Jan 22 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.0-1.20150122git0c2e1aa
- Initial version
