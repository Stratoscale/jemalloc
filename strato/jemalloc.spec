%global strato_ver 1

Name:           jemalloc
Version:        4.2.1

Release:        1.s%{?strato_ver}%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.canonware.com/jemalloc/
Source0:        https://github.com/jemalloc/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  /usr/bin/xsltproc
%ifnarch s390
BuildRequires:  valgrind-devel
%endif

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
autoconf

#% patch2 -p1 -b .armv5tel
%ifarch ppc ppc64
%if 0%{?rhel} == 5
%patch3 -b .ppc
%patch4 -b .ppc
%endif
%endif

%build
%ifarch i686
%if 0%{?fedora} >= 21
CFLAGS="%{optflags} -msse2"
%endif
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
export LDFLAGS="%{?__global_ldflags} -lrt"
%endif

CFLAGS="$RPM_OPT_FLAGS -funroll-loops"

%configure
make dist
make %{?_smp_mflags}
%check
make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Install this with doc macro instead
rm %{buildroot}%{_datadir}/doc/%{name}/jemalloc.html

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/libjemalloc.so.*
%{_bindir}/jemalloc.sh
%{_bindir}/jemalloc-config
%{_bindir}/jeprof
%{_libdir}/pkgconfig/jemalloc.pc
%doc COPYING README VERSION
%doc doc/jemalloc.html
%ifarch ppc ppc64
%if 0%{?rhel} == 5
%doc COPYING.epel5-ppc
%endif
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Wed Jul 06 2016 Rafael Buchbinder <rafi@stratoscale.com> - 4.2.1-1s1
- Update to 4.2.1

