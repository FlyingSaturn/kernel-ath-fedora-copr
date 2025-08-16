# Spec file for building an x86_64 mainline Linux kernel with a custom configuration.
# This file is for a personal or test build and is not a full-featured Fedora kernel spec.
# Author: Bhargavjit Bhuyan
# Corrected by: Gemini
# Note: This spec file has been simplified to remove non-essential
# build dependencies for a basic test build.

# REVERTED: Versioning restored to the original scheme.
%global mainline_version 6
%global mainline_subversion 16
%global patchlevel 1
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
Source0: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.16.1.tar.xz
Source1: https://github.com/FlyingSaturn/kernel-ath-fedora-copr/raw/refs/heads/main/second-config.config
Source2: https://github.com/FlyingSaturn/kernel-ath-fedora-copr/raw/refs/heads/main/aspm-fix.patch
Patch0: %{SOURCE2}


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
BuildRequires: git
BuildRequires: gnupg2
BuildRequires: openssl
BuildRequires: rsync
BuildRequires: dracut
BuildRequires: rpmdevtools 
BuildRequires: rpmlint
BuildRequires: hostname
BuildRequires: elfutils-devel
BuildRequires: dwarves
BuildRequires: perl

# CONFIRMED: Build is exclusively for x86_64.
ExclusiveArch: x86_64

%description
Custom-built mainline Linux kernel for x86_64 testing.

%prep
%autosetup -n linux-%{version} -p1

%build
# Use the default configuration and build the kernel and its modules
cp %{SOURCE1} ./.config
make olddefconfig
#NPROCS=$(/usr/bin/getconf _NPROCESSORS_ONLN)
BUILD_DATE=$(date +%Y%m%d)
make -j$(nproc) binrpm-pkg LOCALVERSION=-patchtest${BUILD_DATE}

%files
rpmbuild/RPMS/*.x86_64.rpm


%changelog
* Fri Aug 15 2025 FlyingSaturn and Bhargavjit Bhuyan <you@example.com> - 6.16.1-2
  - Making RPM output-based builds
