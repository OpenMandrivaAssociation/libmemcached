%define	major 11
%define	util_major 2
%define	hashkit_major 2
%define libname %mklibname memcached %{major}
%define util_libname %mklibname memcachedutil %{util_major}
%define protocol_libname %mklibname memcachedprotocol 0
%define hashkit_libname %mklibname memcachedhashkit %{hashkit_major}
%define devname %mklibname memcached -d

Summary:	A memcached C library and command line tools
Name:		libmemcached
Version:	1.1.4
Release:	1
Group:		System/Libraries
License:	BSD
Url:		https://libmemcached.org/
Source0:   https://github.com/awesomized/libmemcached/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz           
#Source0:	https://launchpad.net/libmemcached/1.0/%{version}/+download/libmemcached-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:        bison
BuildRequires:        flex
BuildRequires:	libtool
BuildRequires:	memcached >= 1.4.9
BuildRequires:	perl-devel
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(libevent)

%description
libmemcached is a C client library to interface to a memcached server. It has
been designed to be light on memory usage, thread safe, and to provide full
access to server side methods. It also implements several command line tools:

memcat - Cat a set of key values to stdout
memcp - Copy a set of files to a memcached cluster
memdump - Dump all values from one or many servers
memerror - Translate a memcached errror code into a string
memexist - Erase a key or set of keys from a memcached cluster
memflush - Erase all data in a server of memcached servers
memping - Ping a server to see if it is alive
memrm - Erase a key or set of keys from a memcached cluster
memslap - Generates a load against a memcached custer of servers
memstat - Output the state of a memcached cluster
memtouch - Update the expiration value of an alreasy existing value in the 
           server

%package -n	%{libname}
Summary:	A memcached C library
Group:          System/Libraries
Obsoletes:	%{protocol_libname} < %{EVRD}

%description -n	%{libname}
libmemcached is a C client library to interface to a memcached server. It has
been designed to be light on memory usage, thread safe, and to provide
full access to server side methods.

%package -n	%{util_libname}
Summary:	A memcached C library
Group:          System/Libraries

%description -n	%{util_libname}
libmemcached is a C client library to interface to a memcached server. It has
been designed to be light on memory usage, thread safe, and to provide
full access to server side methods.

%package -n	%{hashkit_libname}
Summary:	A memcached C library
Group:          System/Libraries

%description -n	%{hashkit_libname}
libmemcached is a C client library to interface to a memcached server. It has
been designed to be light on memory usage, thread safe, and to provide
full access to server side methods.

%package -n	%{devname}
Summary:	Static library and header files for the libmemcached library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{util_libname} = %{version}-%{release}
Requires:	%{hashkit_libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
libmemcached is a C client library to interface to a memcached server. It has
been designed to be light on memory usage, thread safe, and to provide
full access to server side methods.

This package contains the static libmemcached library and its header files.

%prep
%setup -q
%autopatch -p1

%build
%cmake

%make_build
%install
%make_install -C build

# (oe) avoid pulling 32 bit libraries on 64 bit arch
%if "%{_lib}" == "lib64"
sed -i -e "s|-L/usr/lib\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/pkgconfig/*.pc
%endif

# Remove unwanted file          
rm -f %{buildroot}%{_libdir}/libp9y.a           

%files
%doc %{_datadir}/doc/libmemcached-awesome/
%{_bindir}/memaslap
%{_bindir}/memcapable
%{_bindir}/memcat
%{_bindir}/memcp
%{_bindir}/memdump
%{_bindir}/memerror
%{_bindir}/memexist
%{_bindir}/memflush
%{_bindir}/memparse
%{_bindir}/memping
%{_bindir}/memrm
%{_bindir}/memslap
%{_bindir}/memstat
%{_bindir}/memtouch
%{_datadir}/libmemcached-awesome/example.cnf           

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog NEWS README* TODO
%{_libdir}/libmemcached.so.%{major}*
%{_libdir}/libmemcachedprotocol.so.0*  
%optional %{_mandir}/man3/libmemcached.3*

%files -n %{util_libname}
%{_libdir}/libmemcachedutil.so.%{util_major}*
%optional %{_mandir}/man3/libmemcachedutil.3*

%files -n %{hashkit_libname}
%{_libdir}/libhashkit.so.%{hashkit_major}*

%files -n %{devname}
%dir %{_includedir}/libhashkit
%dir %{_includedir}/libhashkit-1.0
%dir %{_includedir}/libmemcached
%dir %{_includedir}/libmemcached-1.0
%dir %{_includedir}/libmemcachedutil-1.0
%{_includedir}/libmemcachedprotocol-0.0/           
%{_includedir}/libhashkit/*
%{_includedir}/libhashkit-1.0/*
%{_includedir}/libmemcached/*
%{_includedir}/libmemcached-1.0/*
%{_includedir}/libmemcachedutil-1.0/*
%{_datadir}/aclocal/ax_libmemcached.m4
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/libmemcached-awesome/
#exclude %{_mandir}/man3/libmemcached.3*
#exclude %{_mandir}/man3/libmemcachedutil.3*
%optional %{_mandir}/man3/*

