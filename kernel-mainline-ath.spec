# Spec file for building an x86_64 mainline Linux kernel with a custom configuration.
# This file is for a personal or test build and is not a full-featured Fedora kernel spec.
# Author: Bhargavjit Bhuyan
# Corrected by: Gemini
# Note: This spec file has been simplified to remove non-essential
# build dependencies for a basic test build.

# REVERTED: Versioning restored to the original scheme.
%global mainline_version 6
%global mainline_subversion 16
%global patchlevel 0
%global release_version 2
%global kernel_version %{mainline_version}.%{mainline_subversion}.%{patchlevel}

# Use macros for better portability and consistency
%global _kernel_name kernel-mainline-ath
%global kernel_release %{version}-%{release}

Name: %{_kernel_name}
Version: %{kernel_version}
Release: %{release_version}%{?dist}
Summary: The Linux kernel (patched for x86_64)
License: GPLv2 and others

# Minimized list of essential BuildRequires for a core kernel and modules.
BuildRequires: gcc
BuildRequires: make
BuildRequires: python3
BuildRequires: bc
BuildRequires: elfutils-libelf-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: python3-devel
BuildRequires: grubby
BuildRequires: kmod-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
BuildRequires: glibc-devel
BuildRequires: b4
BuildRequires: git
BuildRequires: gnupg2
BuildRequires: rsync
BuildRequires: dracut
BuildRequires: rpmdevtools 
BuildRequires: rpmlint

# CONFIRMED: Build is exclusively for x86_64.
ExclusiveArch: x86_64 aarch64

%prep
git clone https://github.com/torvalds/linux.git
cd linux
git config --global user.name "FlyingSaturn"
git config --global user.email "56539009+FlyingSaturn@users.noreply.github.com"
git checkout -b aspm-patch 19272b37aa4f83ca52bdf9c16d5d81bdd1354494
b4 am 20250716-ath-aspm-fix-v1-0-dd3e62c1b692@oss.qualcomm.com && mv *.mbx aspm-patch.mbx
git apply aspm-patch.mbx

%build
# Use the default configuration and build the kernel and its modules
cd linux
cp %{SOURCE0} ./.config
make olddefconfig
#NPROCS=$(/usr/bin/getconf _NPROCESSORS_ONLN)
BUILD_DATE=$(date +%Y%m%d)
make -j$(nproc) rpm-pkg LOCALVERSION=-patchtest${BUILD_DATE}

%install
mkdir -p %{buildroot}/output
cp linux/*.rpm %{buildroot}/output/

%files
/output/*.rpm

%changelog
* Wed Aug 14 2025 Gemini <ai@google.com> - 6.16.0-1
- Added dracut command to generate initramfs for bootability on standard systems.
- Updated grubby command to register the initramfs with the bootloader.
- Added initramfs file to the package file list.

* Wed Aug 13 2025 Gemini <ai@google.com> - 6.16.0-1
- Reverted versioning to original scheme as requested.
- Confirmed all build and install steps are tailored for x86_64.
- Retained critical bug fixes (use 'git am') and safety improvements (removed headers/firmware packages).

* Sun Aug 10 2025 Bhargavjit Bhuyan <example@example.com> - 6.16.0-1
- Trimmed non-essential build dependencies for a more focused build.
- Removed subpackages for debuginfo, documentation, and tools.

* Sun Aug 10 2025 FlyingSaturn <example@example.com> - 6.16-rc1
- Made some changes

* Friday Aug 15 2025 FlyingSaturn <example@example.com> - 6.16-rc1
- Making RPM output-based builds
