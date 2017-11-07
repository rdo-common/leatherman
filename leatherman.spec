%if 0%{?epel}
%global boost_version 157
%else
# CentOS SIGs have newer //-installable Boost
%global boost_version 159
%endif

Name:           leatherman
Version:        1.3.0
Release:        4%{?dist}
Summary:        A collection of C++ and CMake utility libraries

# leatherman is ASL 2.0
# bundled rapidjson is MIT

License:        ASL 2.0 and MIT
URL:            https://github.com/puppetlabs/leatherman
Source0:        https://github.com/puppetlabs/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# This unbundles boost-nowide and the boost libraries do not need
# to have the path to nowide added as it's included already
Patch0:         shared_nowide.patch

%if 0%{?fedora}
BuildRequires:  boost-devel
BuildRequires:  cmake
%else
# this isn't in EPEL yet ... but it will be soon
BuildRequires:  boost%{?boost_version}-devel
BuildRequires:  cmake3
%endif
#BuildRequires:  catch-devel
BuildRequires:  curl-devel
BuildRequires:  gettext
BuildRequires:  boost-nowide-devel

%description
A collection of C++ and CMake utility libraries

%package        devel
Summary:        Development files for %{name}
# Building againse leatherman requires the boost nowide headers present
Requires:       boost-nowide-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
# unbundle nowide
rm -rf vendor/nowide
# leatherman isn't compatible with rapidjson 1.1.0 yet so that has to be left bundled for now
# https://tickets.puppetlabs.com/browse/LTH-130
# catch is only used in testing so can be ignored

%build
%if 0%{?fedora}
  %cmake \
%else
  %cmake3 -DBOOST_INCLUDEDIR=/usr/include/boost%{?boost_version} \
          -DBOOST_LIBRARYDIR=%{_libdir}/boost%{?boost_version} \
%endif
          -DLEATHERMAN_SHARED=ON \
	        -DLEATHERMAN_DEBUG=ON

%make_build

%install
%make_install
%if !0%{?fedora}
mkdir -p %{buildroot}%{_libdir}/cmake3
mv %{buildroot}%{_libdir}/cmake/%{name} %{buildroot}%{_libdir}/cmake3/%{name}
%endif
find %{buildroot} -name '*.la' -exec rm -f {} ';'
%find_lang %{name}_logging
%find_lang %{name}_locale

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}_logging.lang  -f %{name}_locale.lang
%license LICENSE
%{_libdir}/%{name}*.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}*.so
%if 0%{?fedora}
%{_libdir}/cmake/%{name}
%else
%{_libdir}/cmake3/%{name}
%endif


%changelog
* Tue Nov 07 2017 James Hogarth <james.hogarth@gmail.com> - 1.3.0-4
- Restore catch to devel build (bz#1510392)
- Use make_build macro as per review

* Sun Oct 29 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1.3.0-3
- Merge with James spec + keep compatibility with CentOS SIGs

* Thu Oct 19 2017 James Hogarth <james.hogarth@gmail.com> - 1.3.0-2
- rebuilt

* Wed Oct 04 2017 James Hogarth <james.hogarth@gmail.com> - 1.3.0-1
- Upstream update
- unbundle nowide

* Thu Aug 31 2017 James Hogarth <james.hogarth@gmail.com> - 1.2.0-1
- Upstream update

* Sat Feb  4 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 0.10.2-1
- Upstream 0.10.2
- Add Fedora support

* Thu Oct 27 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.2-1
- Initial package on EL7

