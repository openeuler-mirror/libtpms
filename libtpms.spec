# --- libtpm rpm-spec ---
%global gitdate     20200710
%global gitcommit   1d392d466a14234b2c0751ed6c22491836691166
%global gitshortcommit  %(c=%{gitcommit}; echo ${c:0:7})


%define name      libtpms
%define versionx   0.7.3
%define release   2

# Valid crypto subsystems are 'freebl' and 'openssl'
%if "%{?crypto_subsystem}" == ""
%define crypto_subsystem openssl
%endif

# Valid build types are 'production' or 'debug'
%define build_type  production

Summary: Library providing Trusted Platform Module (TPM) functionality
Name:           %{name}
Version:        %{versionx}
Release:        2
License:        BSD
Group:          Development/Libraries
Url:            http://github.com/stefanberger/libtpms
Source0:        %{url}/archive/%{gitcommit}/%{name}-%{gitshortcommit}.tar.gz
Provides:       libtpms-%{crypto_subsystem} = %{version}-%{release}

%if "%{crypto_subsystem}" == "openssl"
BuildRequires:  openssl-devel
%else
BuildRequires:  nss-devel >= 3.12.9-2
BuildRequires:  nss-softokn-freebl-devel >= 3.12.9-2
%if 0%{?rhel} > 6 || 0%{?fedora} >= 13
BuildRequires:  nss-softokn-freebl-static >= 3.12.9-2
%endif
BuildRequires:  nss-softokn-devel >= 3.12.9-2, gmp-devel
%endif
BuildRequires:  pkgconfig gawk sed
BuildRequires:  automake autoconf libtool bash coreutils gcc-c++

%if "%{crypto_subsystem}" == "openssl"
Requires:       openssl
%else
Requires:       nss-softokn-freebl >= 3.12.9-2, nss-softokn >= 3.12.9-2
%endif
Requires:       gmp

%description
A library providing TPM functionality for VMs. Targeted for integration
into Qemu.

%package        devel
Summary:        Include files for libtpms
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description   devel
Libtpms header files and documentation.

%files
%defattr(-, root, root, -)
%{_libdir}/%{name}.so.%{version}
%{_libdir}/%{name}.so.0
%doc LICENSE README CHANGES

%files devel
%defattr(-, root, root, -)

%{_libdir}/%{name}.so
%dir %{_includedir}/%{name}
%attr(644, root, root) %{_libdir}/pkgconfig/*.pc
%attr(644, root, root) %{_includedir}/%{name}/*.h
%attr(644, root, root) %{_mandir}/man3/*

%prep
%autosetup -n %{name}-%{gitcommit}

%build

%if "%{crypto_subsystem}" == "openssl"
%define _with_openssl --with-openssl
%endif

%if %{build_type} == debug
%define _enable_debug --enable-debug
%endif

%if %{build_type} == debug
CFLAGS=-O0
%endif
./autogen.sh \
        --with-tpm2 \
        --disable-static \
        --prefix=/usr \
        --libdir=%{_libdir} \
        %{?_with_openssl} \
        %{?_enable_debug}

make %{?_smp_mflags}

%check
make check

%install
install -d -m 0755 $RPM_BUILD_ROOT%{_libdir}
install -d -m 0755 $RPM_BUILD_ROOT%{_includedir}/libtpms
install -d -m 0755 $RPM_BUILD_ROOT%{_mandir}/man3

make %{?_smp_mflags} install DESTDIR=${RPM_BUILD_ROOT}

rm -f $RPM_BUILD_ROOT%{_libdir}/libtpms.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Mon Sep 14 2020 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-2
- update spec file including source0 and update source file 

* Fri Aug 21 2020 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-1
- Package init
- Version of library is now 0.7.3
