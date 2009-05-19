%define	major 2
%define libname %mklibname memcached %{major}
%define develname %mklibname memcached -d

Summary:	A memcached C library and command line tools
Name:		libmemcached
Version:	0.29
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://tangent.org/552/libmemcached.html
Source0:	http://download.tangent.org/%{name}-%{version}.tar.gz
Patch0:		libmemcached-0.29-linkage_fix.diff
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	memcached
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libmemcached is a C client library to interface to a memcached server.
It has been designed to be light on memory usage, thread safe, and to provide
full access to server side methods. It also implements several command line
tools:memcat, memflush, memrm, memstat, and memslap (load generation).

It also implements several command line tools:

memcat - Copy the value of a key to standard output
memflush - Flush the contents of your servers.
memrm - Remove a key(s) from the serrver.
memstat - Dump the stats of your servers to standard output
memslap - Generate testing loads on a memcached cluster

%package -n	%{libname}
Summary:	A memcached C library
Group:          System/Libraries

%description -n	%{libname}
libmemcached is a C client library to interface to a memcached server.
It has been designed to be light on memory usage, thread safe, and to provide
full access to server side methods. It also implements several command line
tools:memcat, memflush, memrm, memstat, and memslap (load generation).

%package -n	%{develname}
Summary:	Static library and header files for the libmemcached library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	memcached-devel = %{version}-%{release}
Obsoletes:	memcached-devel

%description -n	%{develname}
libmemcached is a C client library to interface to a memcached server.
It has been designed to be light on memory usage, thread safe, and to provide
full access to server side methods. It also implements several command line
tools:memcat, memflush, memrm, memstat, and memslap (load generation).

This package contains the static libmemcached library and its header files.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

%build
autoreconf -fis
%configure2_5x \
    --with-memcached=%{_sbindir}/memcached
  
%make

# (oe Fri Jan 30 06:59:18 CET 2009) tests requires root permissions, but don't pass anyway...
#%%check
#make test

%install
rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/memcat
%{_bindir}/memcp
%{_bindir}/memerror
%{_bindir}/memflush
%{_bindir}/memrm
%{_bindir}/memslap
%{_bindir}/memstat
%{_mandir}/man1/memcat.1*
%{_mandir}/man1/memcp.1*
%{_mandir}/man1/memerror.1*
%{_mandir}/man1/memflush.1*
%{_mandir}/man1/memrm.1*
%{_mandir}/man1/memslap.1*
%{_mandir}/man1/memstat.1*

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.%{major}*
%{_libdir}/libmemcachedutil.so.0*
%{_mandir}/man3/libmemcached.3*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%exclude %{_mandir}/man3/libmemcached.3*
%{_mandir}/man3/*
