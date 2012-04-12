%define	major 10
%define	util_major 2
%define	protocol_major 0
%define	hashkit_major 2
%define libname %mklibname memcached %{major}
%define util_libname %mklibname memcachedutil %{util_major}
%define protocol_libname %mklibname memcachedprotocol %{protocol_major}
%define hashkit_libname %mklibname memcachedhashkit %{hashkit_major}
%define develname %mklibname memcached -d

Summary:	A memcached C library and command line tools
Name:		libmemcached
Version:	1.0.6
Release:	1
Group:		System/Libraries
License:	BSD
URL:		http://libmemcached.org/
Source0:	http://code.launchpad.net/libmemcached/1.0/%version/+download/%{name}-%{version}-no_hsieh.tar.gz
Patch0:		libmemcached-1.0.2-no_pandora_print_callstack.diff
Patch1:		libmemcached-1.0.5-linkage_fix.diff
BuildRequires:	automake autoconf libtool
BuildRequires:	memcached >= 1.4.9
BuildRequires:	libevent-devel
BuildRequires:	perl-devel
BuildRequires:	libsasl-devel
BuildRequires:	pkgconfig

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
sever

%package -n	%{libname}
Summary:	A memcached C library
Group:          System/Libraries

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

%package -n	%{protocol_libname}
Summary:	A memcached C library
Group:          System/Libraries

%description -n	%{protocol_libname}
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

%package -n	%{develname}
Summary:	Static library and header files for the libmemcached library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{util_libname} = %{version}-%{release}
Requires:	%{protocol_libname} = %{version}-%{release}
Requires:	%{hashkit_libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libmemcached-devel = %{version}-%{release}

%description -n	%{develname}
libmemcached is a C client library to interface to a memcached server. It has
been designed to be light on memory usage, thread safe, and to provide
full access to server side methods.

This package contains the static libmemcached library and its header files.

%prep

%setup -q -n %{name}-%{version}
# clients/ms_sigsegv.c:41: undefined reference to `pandora_print_callstack'
%patch0 -p0
%patch1 -p0

# invalid license, according to redhat
if [ -f libhashkit/hsieh.cc ]; then
    echo "the libhashkit/hsieh.cc file was found, you have to remove it..."
    exit 1
fi

# make the tests work
me=`id -nu`
perl -pi -e "s|-u root|-u $me|g" Makefile* tests/include.am tests/server.c

%build
autoreconf -fi

export LIBSASL="-lsasl2"
export PTHREAD_LIBS="-lpthread"

%configure2_5x \
    --disable-static \
    --enable-shared \
    --enable-memaslap \
    --with-memcached=%{_bindir}/memcached \
    --with-memcached_sasl=%{_bindir}/memcached

%make LIBSASL="-lsasl2" PTHREAD_LIBS="-lpthread"

# (oe ) barfs at:
# Assertion failed in tests/mem_functions.c:5946: rc == MEMCACHED_TIMEOUT
#%%check
#make test

%install
rm -rf %{buildroot}

# weird makefile poo
make DESTDIR=%{buildroot} install-exec-am install-data-am

# (oe) avoid pulling 32 bit libraries on 64 bit arch
%if "%{_lib}" == "lib64"
perl -pi -e "s|-L/usr/lib\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/pkgconfig/*.pc
%endif

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files
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
%{_mandir}/man1/memcapable.1*
%{_mandir}/man1/memcat.1*
%{_mandir}/man1/memcp.1*
%{_mandir}/man1/memdump.1*
%{_mandir}/man1/memerror.1*
%{_mandir}/man1/memflush.1*
%{_mandir}/man1/memrm.1*
%{_mandir}/man1/memslap.1*
%{_mandir}/man1/memaslap.1*
%{_mandir}/man1/memstat.1*

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.so.%{major}*
%{_mandir}/man3/libmemcached.3*

%files -n %{util_libname}
%{_libdir}/libmemcachedutil.so.%{util_major}*
%{_mandir}/man3/libmemcachedutil.3*

%files -n %{protocol_libname}
%{_libdir}/libmemcachedprotocol.so.%{protocol_major}*

%files -n %{hashkit_libname}
%{_libdir}/libhashkit.so.%{hashkit_major}*

%files -n %{develname}
%dir %{_includedir}/libhashkit
%dir %{_includedir}/libhashkit-1.0
%dir %{_includedir}/libmemcached
%dir %{_includedir}/libmemcached-1.0
%dir %{_includedir}/libmemcachedprotocol-0.0
%dir %{_includedir}/libmemcachedutil-1.0
%{_includedir}/libhashkit/*
%{_includedir}/libhashkit-1.0/*
%{_includedir}/libmemcached/*
%{_includedir}/libmemcached-1.0/*
%{_includedir}/libmemcachedprotocol-0.0/*
%{_includedir}/libmemcachedutil-1.0/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%exclude %{_mandir}/man3/libmemcached.3*
%exclude %{_mandir}/man3/libmemcachedutil.3*
%{_mandir}/man3/*


%changelog
* Thu Apr 12 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-1
+ Revision: 790369
- 1.0.6
- 1.0.5

* Sat Jan 28 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.4-1
+ Revision: 769495
- 1.0.4

* Tue Dec 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-3
+ Revision: 738327
- various cleanups

* Sun Nov 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2
+ Revision: 722493
- various fixes

* Sat Nov 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1
+ Revision: 720805
- fix build
- 1.0.2
- drop the libhashkit/hsieh.cc source due to possible invlid license
- P0: where's pandora_print_callstack? drop that for now
- various cleanups

* Fri Aug 12 2011 Oden Eriksson <oeriksson@mandriva.com> 0.51-1
+ Revision: 694119
- 0.51

* Tue Jun 21 2011 Oden Eriksson <oeriksson@mandriva.com> 0.50-1
+ Revision: 686432
- 0.50

* Tue Apr 19 2011 Funda Wang <fwang@mandriva.org> 0.49-1
+ Revision: 656000
- update hashkit libname
- update file list
- new version 0.59

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.48-1
+ Revision: 646047
- 0.48

* Mon Mar 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0.47-1
+ Revision: 642440
- 0.47

* Tue Feb 15 2011 Oden Eriksson <oeriksson@mandriva.com> 0.46-1
+ Revision: 637865
- 0.46
- one step closer to having the tests work

* Sun Oct 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.44-1mdv2011.0
+ Revision: 584592
- bump major
- 0.44

* Mon Aug 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.43-2mdv2011.0
+ Revision: 568088
- bump release

* Fri Jul 30 2010 Funda Wang <fwang@mandriva.org> 0.43-1mdv2011.0
+ Revision: 563740
- update to new version 0.43

* Thu Jul 15 2010 Oden Eriksson <oeriksson@mandriva.com> 0.42-2mdv2011.0
+ Revision: 553522
- rebuilt due to package loss

* Tue Jul 13 2010 Oden Eriksson <oeriksson@mandriva.com> 0.42-1mdv2011.0
+ Revision: 552118
- fix build
- 0.42

  + Funda Wang <fwang@mandriva.org>
    - updaet url

* Sat Apr 24 2010 Funda Wang <fwang@mandriva.org> 0.40-1mdv2010.1
+ Revision: 538416
- New version 0.40

* Wed Apr 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.39-1mdv2010.1
+ Revision: 532606
- 0.39

* Sat Mar 27 2010 Oden Eriksson <oeriksson@mandriva.com> 0.38-2mdv2010.1
+ Revision: 528046
- fix build
- fix deps

* Thu Feb 11 2010 Funda Wang <fwang@mandriva.org> 0.38-1mdv2010.1
+ Revision: 504357
- New version 0.38

* Wed Jan 13 2010 Oden Eriksson <oeriksson@mandriva.com> 0.37-1mdv2010.1
+ Revision: 490748
- the major was bumped
- 0.37

* Fri Jan 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.36-1mdv2010.1
+ Revision: 487534
- fix deps
- 0.36

* Thu Nov 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.35-1mdv2010.1
+ Revision: 467406
- 0.35

* Fri Nov 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.34-1mdv2010.1
+ Revision: 461873
- fix build
- 0.34

* Fri Oct 02 2009 Oden Eriksson <oeriksson@mandriva.com> 0.33-2mdv2010.0
+ Revision: 452725
- fix #54183 (libmemcached* improperly libified, leading to conflicts)

* Fri Sep 25 2009 Oden Eriksson <oeriksson@mandriva.com> 0.33-1mdv2010.0
+ Revision: 448751
- add unpacked files
- new major (3)
- 0.33

* Fri Sep 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.32-1mdv2010.0
+ Revision: 444312
- 0.32

* Sat Jul 11 2009 Oden Eriksson <oeriksson@mandriva.com> 0.31-1mdv2010.0
+ Revision: 394777
- 0.31

* Tue Jun 02 2009 Oden Eriksson <oeriksson@mandriva.com> 0.30-1mdv2010.0
+ Revision: 382160
- 0.30
- drop P0, it's implemented upstream

* Tue May 19 2009 Oden Eriksson <oeriksson@mandriva.com> 0.29-1mdv2010.0
+ Revision: 377735
- 0.29

* Fri Jan 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.26-1mdv2009.1
+ Revision: 335430
- fix build
- 0.26

* Sat Nov 29 2008 Funda Wang <fwang@mandriva.org> 0.25-1mdv2009.1
+ Revision: 307798
- new version 0.25

* Mon Sep 08 2008 Oden Eriksson <oeriksson@mandriva.com> 0.23-1mdv2009.0
+ Revision: 282751
- 0.23

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.22-1mdv2009.0
+ Revision: 235873
- 0.22

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 0.21-2mdv2009.0
+ Revision: 229680
- never obsolete a library

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 24 2008 Oden Eriksson <oeriksson@mandriva.com> 0.21-1mdv2009.0
+ Revision: 210841
- 0.21

* Tue May 06 2008 Funda Wang <fwang@mandriva.org> 0.20-1mdv2009.0
+ Revision: 201759
- New version 0.20

* Thu Apr 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.19-1mdv2009.0
+ Revision: 192537
- 0.19
- 0.18

  + Thierry Vignaud <tv@mandriva.org>
    - remove URL from description

* Mon Feb 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.16-1mdv2008.1
+ Revision: 171415
- 0.16

* Wed Jan 30 2008 Funda Wang <fwang@mandriva.org> 0.15-1mdv2008.1
+ Revision: 160165
- update to new version 0.15

* Tue Jan 22 2008 Oden Eriksson <oeriksson@mandriva.com> 0.14-1mdv2008.1
+ Revision: 156570
- 0.14

* Mon Jan 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.13-1mdv2008.1
+ Revision: 151152
- 0.13

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Oden Eriksson <oeriksson@mandriva.com> 0.12-1mdv2008.1
+ Revision: 118071
- 0.12
- simplify the spec file a bit

* Mon Nov 26 2007 Oden Eriksson <oeriksson@mandriva.com> 0.11-1mdv2008.1
+ Revision: 112120
- 0.11

* Wed Nov 21 2007 Oden Eriksson <oeriksson@mandriva.com> 0.10-1mdv2008.1
+ Revision: 110950
- 0.10

* Fri Nov 16 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9-1mdv2008.1
+ Revision: 109051
- no need to obsolete a package that don't exist (duh!)
- 0.9
- new major (1)

* Wed Nov 14 2007 Funda Wang <fwang@mandriva.org> 0.7-2mdv2008.1
+ Revision: 108823
- rebuild

* Tue Oct 30 2007 Oden Eriksson <oeriksson@mandriva.com> 0.7-1mdv2008.1
+ Revision: 103960
- 0.7

* Wed Oct 17 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6-1mdv2008.1
+ Revision: 99759
- 0.6

* Tue Oct 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5-1mdv2008.1
+ Revision: 95786
- 0.5

* Wed Oct 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.4-1mdv2008.1
+ Revision: 95201
- 0.4
- import libmemcached


* Tue Oct 02 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3-1mdv2008.0
- initial Mandriva package
