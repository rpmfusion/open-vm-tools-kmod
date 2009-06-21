# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

%define tname open-vm-tools
%define builddate 2009.03.18
%define buildver 154848
%define ovtmodules vmblock vmci vmhgfs vmmemctl vmsync vmxnet vmxnet3 vsock pvscsi

Name:      open-vm-tools-kmod
Version:   0.0.0.%{buildver}
Release:   1%{?dist}.10
Summary:   VMware Tools Kernel Modules
Group:     System Environment/Kernel
License:   GPLv2
URL:       http://open-vm-tools.sourceforge.net/
Source0:   http://downloads.sourceforge.net/%{tname}/%{tname}-%{builddate}-%{buildver}.tar.gz
Source11:  %{tname}-excludekernel-filterfile
BuildRoot: %{_tmppath}/%{name}-%{builddate}-%{release}-root-%(%{__id_u} -n)

# VMWare only supports x86 architectures.
ExclusiveArch:  i586 i686 x86_64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Open-vm-tools are the open source implementation of VMware Tools. They
are a set of guest operating system virtualization components that
enhance performance and user experience of VMWare virtual
machines. This package contains the kernel modules of open-vm-tools.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -n open-vm-tools-%{builddate}-%{buildver}
for kernel_version  in %{?kernel_versions} ; do
    cp -ar modules/linux _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    for ovtmodule in %{ovtmodules}; do
        make -C ${PWD}/_kmod_build_${kernel_version%%___*}/${ovtmodule} VM_UNAME=${kernel_version%%___*} HEADER_DIR="${kernel_version##*___}/include" CC_OPTS=-DVMW_HAVE_EPOLL
    done
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version  in %{?kernel_versions} ; do
    for ovtmodule in %{ovtmodules}; do
        install -D -m 755 _kmod_build_${kernel_version%%___*}/${ovtmodule}/${ovtmodule}.ko $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/${ovtmodule}.ko
    done
done
# akmods:
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.10
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.9
- rebuild for new kernels

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.8
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.7
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.6
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.5
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.4
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.3
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.2
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.154848-1.1
- rebuild for new kernels

* Mon Mar 23 2009  <denis@poolshark.org> - 0.0.0.154848-1
- Update to upstream build 154848

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.142982-1.2
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.142982-1.1
- rebuild for latest Fedora kernel;

* Wed Jan 28 2009 Denis Leroy <denis@poolshark.org> - 0.0.0.142982-1
- Update to upstream build 142982

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.137496-2.2
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.137496-2.1
- rebuild for latest Fedora kernel;

* Tue Jan 13 2009 Denis Leroy <denis@poolshark.org> - 0.0.0.137496-2
- Added patch to fix compilation with latest rawhide kernel

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.137496-1.1
- rebuild for latest Fedora kernel;

* Sat Jan 10 2009 Denis Leroy <denis@poolshark.org> - 0.0.0.137496-1
- Update to upstream build 137496

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.130226-1.4
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.130226-1.3
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.130226-1.2
- rebuild for latest Fedora kernel;

* Thu Dec 18 2008 Denis Leroy <denis@poolshark.org> - 0.0.0.130226-1.1
- Update to upstream 130226
- Added new kernel module pvscsi

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.123053-1.6
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.123053-1.5
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.123053-1.4
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.123053-1.3
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.0.123053-1.2
- rebuild for latest Fedora kernel;

* Mon Oct 27 2008 Denis Leroy <denis@poolshark.org> - 0.0.0.123053-1.1
- Small fixes for kmod2 compliance all over the place
- Changed version and EVR formats

* Wed Oct 15 2008 Denis Leroy <denis@poolshark.org> - 0-1.2008.10.10
- First kmod draft
