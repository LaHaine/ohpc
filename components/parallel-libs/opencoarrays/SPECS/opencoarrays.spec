#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

# Build that is dependent on compiler/mpi toolchains
%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname opencoarrays
%define oname OpenCoarrays
Summary: Opencoarray Fortran
Name: %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version: 2.0.0
Release: 1
Source0: https://github.com/sourceryinstitute/OpenCoarrays/releases/download/%version/OpenCoarrays-%version.tar.gz
Source1: OHPC_macros
License: BSD
Group: Development/Languages
Url: http://www.opencoarrays.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: cmake-ohpc
BuildRequires: openssh-clients

# Default library install path
%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%version

%description
OpenCoarrays is an open-source software project that supports the
coarray Fortran (CAF) parallel programming features of the Fortran
2008 standard and several features proposed for Fortran 2015 in the
draft Technical Specification TS 18508 Additional Parallel Features in
Fortran.

%prep
%setup -q -n %oname-%version
%build

%install
rm -rf $RPM_BUILD_ROOT
export LDFLAGS=-Wl,--build-id
# OpenHPC compiler/mpi designation
%ohpc_setup_compiler
module add cmake
./install.sh -y %{_smp_mflags}  -i %{buildroot}/%install_path

#remove buildroot
grep -rl %buildroot %buildroot|xargs perl -pi -e "s^%buildroot^^" 
cd %buildroot/%install_path/include
ln -sf OpenCoarrays*/opencoarrays.mod .

mkdir -p %buildroot/opt/ohpc/pub/moduledeps/%{compiler_family}-%{mpi_family}/%pname
cat > %buildroot/opt/ohpc/pub/moduledeps/%{compiler_family}-%{mpi_family}/%pname/%{version} << EOF
#%Module 1.0
#
#  Opencoarrays Fortran Compiler module for use with 'lmod-ohpc'
#  package:
# 
proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the opencoarrays wrapper built with the %{compiler_family}"
puts stderr "compiler toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"
}
module-whatis  "Setup Opencoarrays compiler suite version %version"
prepend-path 		PATH 		 %{install_path}/bin
prepend-path            LD_LIBRARY_PATH  %{install_path}/%_lib/
EOF

%check
cd prerequisites/builds/%pname/%version
%ohpc_setup_compiler
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc *.md
%dir /opt/ohpc/pub/moduledeps/%{compiler_family}-%{mpi_family}/
%dir /opt/ohpc/pub/moduledeps/%{compiler_family}-%{mpi_family}/%pname
/opt/ohpc/pub/moduledeps/%{compiler_family}-%{mpi_family}/%pname
%dir %install_path/
%dir %install_path/bin
%install_path/bin/caf
%install_path/bin/cafrun
%install_path/share/man/man1/caf.1
%install_path/share/man/man1/cafrun.1
%install_path/setup.sh
%install_path/setup.csh
%dir %install_path/%_lib
%install_path/%_lib/cmake
%install_path/%_lib/libcaf_mpi.a
%install_path/%_lib/libcaf_mpi.so*
%dir %install_path/include
%install_path/include/*.h
%install_path/include/OpenCoarrays-%{version}*
%install_path/include/*.mod


%changelog
* Mon Mar 12 2018 Götz Waschk <goetz.waschk@desy.de> 2.0.0-1
- new version 2.0.0 final

* Wed Feb 21 2018 Götz Waschk <goetz.waschk@desy.de> 2.0.0-0.rc1
- build for OpenHPC
- new version

* Wed Jan 31 2018 Götz Waschk <goetz.waschk@desy.de> 1.9.3-1.el7
- add shared library dir to the path
- update file list
- drop patches
- new version

* Thu May 11 2017 Götz Waschk <goetz.waschk@desy.de> 1.8.11-1.el7
- patch wrapper script
- new version

* Tue Apr 11 2017 Götz Waschk <goetz.waschk@desy.de> 1.8.5-2.el7
- remove extra path from setup.[c]sh
- new snapshot

* Tue Apr  4 2017 Götz Waschk <goetz.waschk@desy.de> 1.8.5-1.el7
- new openmpi
- new snapshot

* Mon Feb 06 2017 Götz Waschk <goetz.waschk@desy.de> 1.8.3-1.el6
- initial package

