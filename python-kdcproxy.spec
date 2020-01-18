%global realname kdcproxy

Name:           python-%{realname}
Version:        0.3.2
Release:        2%{?dist}
Summary:        MS-KKDCP (kerberos proxy) WSGI module

License:        MIT
URL:            https://github.com/npmccallum/%{realname}
Source0:        https://github.com/npmccallum/%{realname}/archive/v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

Patch0: Downgrade-socket-problems-to-warnings.patch

%if 0%{?rhel} == 0
BuildRequires:  python-tox
BuildRequires:  pytest
BuildRequires:  python-coverage
BuildRequires:  python-webtest
BuildRequires:  python-pyasn1
BuildRequires:  python-dns
BuildRequires:  python-mock

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-coverage
BuildRequires:  python3-webtest
BuildRequires:  python3-pyasn1
BuildRequires:  python3-dns
BuildRequires:  python3-mock
%endif

Requires:       python-dns
Requires:       python-pyasn1

%description
This package contains a Python 2.x WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.

%if 0%{?rhel} == 0
%package -n python3-%{realname}
Summary:        MS-KKDCP (kerberos proxy) WSGI module
Requires:       python3-dns
Requires:       python3-pyasn1

%description -n python3-%{realname}
This package contains a Python 3.x WSGI module for proxying KDC requests over
HTTP by following the MS-KKDCP protocol. It aims to be simple to deploy, with
minimal configuration.
%endif

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1 -b .Downgrade-socket-problems-to-warnings

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{python_sitelib}/%{realname}/ -name '*.py' -exec chmod 755 '{}' \;

%if 0%{?rhel} == 0
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{python3_sitelib}/%{realname}/ -name '*.py' -exec chmod 755 '{}' \;
%endif

%check
%if 0%{?rhel} == 0
tox --sitepackages -e py27,py34
%endif

%files
%doc COPYING README
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-*.egg-info

%if 0%{?rhel} == 0
%files -n python3-%{realname}
%doc COPYING README
%{python3_sitelib}/%{realname}
%{python3_sitelib}/%{realname}-%{version}-*.egg-info
%endif

%changelog
* Mon Dec 17 2018 Robbie Harwood <rharwood@redhat.com> - 0.3.2-2
- Downgrade socket problems to warnings
- Resolves: #1525925

* Mon Aug 03 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2
- Fixes CVE-2015-5159

* Wed Jul 22 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.3-1
- Update to 0.3
- Run tests in Fedora (not RHEL due to python-tox)

* Fri Oct 24 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Thu Oct 23 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.2-1
- Update to 0.2
- Fix EPEL7 build

* Tue Jan 21 2014 Nathaniel McCallum <npmccallum@fedoraproject.org> - 0.1.1-1
- Initial package
