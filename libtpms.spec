# --- libtpm rpm-spec ---
%global gitdate     20200710
%global gitcommit   1d392d466a14234b2c0751ed6c22491836691166
%global gitshortcommit  %(c=%{gitcommit}; echo ${c:0:7})


%define name      libtpms
%define versionx  0.7.3
%define release   6

# Valid crypto subsystems are 'freebl' and 'openssl'
%if "%{?crypto_subsystem}" == ""
%define crypto_subsystem openssl
%endif

# Valid build types are 'production' or 'debug'
%define build_type  production

Summary: Library providing Trusted Platform Module (TPM) functionality
Name:           %{name}
Version:        %{versionx}
Release:        %{release}
License:        BSD
Group:          Development/Libraries
Url:            http://github.com/stefanberger/libtpms
Source0:        %{url}/archive/%{gitcommit}/%{name}-%{gitshortcommit}.tar.gz
Provides:       libtpms-%{crypto_subsystem} = %{version}-%{release}

Patch0: tpm2-CryptSym-fix-AES-output-IV.patch
Patch1: tpm2-Add-SEED_COMPAT_LEVEL-to-seeds-in.patch
Patch2: tpm2-Add-SEED_COMPAT_LEVEL-to-nullSeed-to-track-comp.patch
Patch3: tpm2-Add-SEED_COMPAT_LEVEL-to-DRBG-state.patch
Patch4: tpm2-rev155-Add-new-RsaAdjustPrimeCandidate-code.patch
Patch5: tpm2-Introduce-SEED_COMPAT_LEVEL_RSA_PRIME_ADJUST_FI.patch
Patch6: tpm2-Pass-SEED_COMPAT_LEVEL-to-CryptAdjustPrimeCandi.patch
Patch7: tpm2-Activate-SEED_COMPAT_LEVEL_RSA_PRIME_ADJUST_FIX.patch
Patch8: tpm2-Initialize-a-whole-OBJECT-before-using-it.patch
Patch9: tpm2-Fix-issue-with-misaligned-address-when-marshall.patch
Patch10: tpm2-NVMarshal-Handle-index-orderly-RAM-without-0-si.patch

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
%setup -n %{name}-%{gitcommit}
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
