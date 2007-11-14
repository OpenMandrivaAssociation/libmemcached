%define	major 0
%define libname %mklibname memcached %{major}
%define develname %mklibname memcached -d

Summary:	A memcached C library and command line tools
Name:		libmemcached
Version:	0.7
Release:	%mkrel 2
Group:		System/Libraries
License:	BSD
URL:		http://tangent.org/552/libmemcached.html
Source0:	http://download.tangent.org/%{name}-%{version}.tar.gz
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
libmemcached is a C client library to interface to a memcached server
(http://danga.com/memcached). It has been designed to be light on memory usage,
thread safe, and to provide full access to server side methods. It also
implements several command line tools:memcat, memflush, memrm, memstat, and
memslap (load generation).

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
libmemcached is a C client library to interface to a memcached server
(http://danga.com/memcached). It has been designed to be light on memory usage,
thread safe, and to provide full access to server side methods. It also
implements several command line tools:memcat, memflush, memrm, memstat, and
memslap (load generation).

%package -n	%{develname}
Summary:	Static library and header files for the libmemcached library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	memcached-devel = %{version}-%{release}
Obsoletes:	memcached-devel

%description -n	%{develname}
libmemcached is a C client library to interface to a memcached server
(http://danga.com/memcached). It has been designed to be light on memory usage,
thread safe, and to provide full access to server side methods. It also
implements several command line tools:memcat, memflush, memrm, memstat, and
memslap (load generation).

This package contains the static libmemcached library and its header files.

%prep

%setup -q -n %{name}-%{version}

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/memcat
%{_bindir}/memcp
%{_bindir}/memflush
%{_bindir}/memrm
%{_bindir}/memstat
%{_bindir}/memslap
%{_mandir}/man1/memcat.1*
%{_mandir}/man1/memcp.1*
%{_mandir}/man1/memflush.1*
%{_mandir}/man1/memrm.1*
%{_mandir}/man1/memslap.1*
%{_mandir}/man1/memstat.1*

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.*
%{_mandir}/man3/libmemcached.3*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_mandir}/man3/libmemcached_examples.3*
%{_mandir}/man3/memcached_add.3*
%{_mandir}/man3/memcached_behavior_get.3*
%{_mandir}/man3/memcached_behavior_set.3*
%{_mandir}/man3/memcached_create.3*
%{_mandir}/man3/memcached_decrement.3*
%{_mandir}/man3/memcached_delete.3*
%{_mandir}/man3/memcached_fetch.3*
%{_mandir}/man3/memcached_free.3*
%{_mandir}/man3/memcached_get.3*
%{_mandir}/man3/memcached_increment.3*
%{_mandir}/man3/memcached_mget.3*
%{_mandir}/man3/memcached_quit.3*
%{_mandir}/man3/memcached_replace.3*
%{_mandir}/man3/memcached_server_add.3*
%{_mandir}/man3/memcached_server_count.3*
%{_mandir}/man3/memcached_server_list.3*
%{_mandir}/man3/memcached_server_list_append.3*
%{_mandir}/man3/memcached_server_list_count.3*
%{_mandir}/man3/memcached_server_list_free.3*
%{_mandir}/man3/memcached_server_push.3*
%{_mandir}/man3/memcached_servers_parse.3*
%{_mandir}/man3/memcached_set.3*
%{_mandir}/man3/memcached_stat.3*
%{_mandir}/man3/memcached_stat_get_keys.3*
%{_mandir}/man3/memcached_stat_get_value.3*
%{_mandir}/man3/memcached_stat_servername.3*
%{_mandir}/man3/memcached_strerror.3*
%{_mandir}/man3/memcached_verbosity.3*
%{_mandir}/man3/memcached_clone.3*
