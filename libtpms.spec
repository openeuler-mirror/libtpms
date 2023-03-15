# --- libtpm rpm-spec ---

%define name      libtpms
%define version   0.9.5
%define release   2

# Valid crypto subsystems are 'freebl' and 'openssl'
%if "%{?crypto_subsystem}" == ""
%define crypto_subsystem openssl
%endif

# Valid build types are 'production' or 'debug'
%define build_type  production

Summary: Library providing Trusted Platform Module (TPM) functionality
Name:           %{name}
Version:        %{version}
Release:        %{release}
License:        BSD
Group:          Development/Libraries
Url:            http://github.com/stefanberger/libtpms
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Provides:       libtpms-%{crypto_subsystem} = %{version}-%{release}

Patch0: 0001-tpm2-Check-size-of-buffer-before-accessing-it-CVE-20.patch

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
%setup -n %{name}-%{version}
%autopatch -p1

%build

%if "%{crypto_subsystem}" == "openssl"
%define _with_openssl --with-openssl
%endif

%if "%{build_type}" == "debug"
%define _enable_debug --enable-debug
%endif

%if "%{build_type}" == "debug"
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
* Tue Mar 07 2023 jiangfangjie <jiangfangjie@huawei.com> - 0.9.5-2
- fix CVE-2023--1018 and CVE-2023-1017

* Fri Feb 03 2023 yezengruan <yezengruan@huawei.com> - 0.9.5-1
- update to version 0.9.5

* Wed May 18 2022 yezengruan <yezengruan@huawei.com> - 0.7.3-7
- tpm2: Reset TPM2B buffer sizes after test fails for valid buffer size
- tpm2: Add maxSize parameter to TPM2B_Marshal for sanity checks
- tpm2: Restore original value if unmarsalled value was illegal
- fix CVE-2021-3623

* Mon Feb 14 2022 imxcc <xingchaochao@huawei.com> - 0.7.3-6
- fix bare word "debug" in spec

* Wed Nov 10 2021 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-5
-TYPE: CVE
-ID:NA
-ID:NA
-DESC: fix CVE-2021-3746

* Tue May 11 2021 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-4
-TYPE: CVE
-ID:NA
-SUG:NA
-DESC:fix CVE-2021-3505

* Mon Apr 5 2021 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-3
- Type:CVE
- ID:NA
- SUG:NA
- DESC: fix CVE-2021-3446

* Mon Sep 14 2020 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-2
- update spec file including source0 and update source file

* Fri Aug 21 2020 jiangfangjie <jiangfangjie@huawei.com> - 0.7.3-1
- Package init
- Version of library is now 0.7.3
