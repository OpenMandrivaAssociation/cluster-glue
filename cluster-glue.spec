%define gname	haclient
%define uname	hacluster
%define nogroup	nobody
%define maj1	1
%define major	2
%define liblrm		%mklibname lrm %{major}
%define libpils		%mklibname pils %{major}
%define libplumb 	%mklibname plumb %{major}
%define libplumbgpl	%mklibname plumbgpl %{major}
%define libstonith	%mklibname stonith %{maj1}
%define devname	%mklibname %{name} -d


# When downloading directly from Mercurial, it will automatically add this prefix
# Invoking 'hg archive' wont but you can add one with: hg archive -t tgz -p "Reusable-Cluster-Components-" -r $upstreamversion $upstreamversion.tar.gz
%define upstreamprefix Reusable-Cluster-Components-glue--
%define upstreamversion glue-%{version}

# Keep around for when/if required
#global alphatag %{upstreamversion}.hg

Summary:	Reusable cluster components
Name:		cluster-glue
Version:	1.0.11
Release:	3
License:	GPLv2+ and LGPLv2+
Url:		http://linux-ha.org/wiki/Cluster_Glue
Group:		System/Libraries
Source0:	http://hg.linux-ha.org/glue/archive/%{upstreamversion}.tar.bz2
Patch0:		cluster-glue-automake-1.13.patch

BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:	bzip2-devel
BuildRequires:	libtool-devel
BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(OpenIPMI)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(uuid)
Requires:	perl-TimeDate

%description
A collection of common tools that are useful for writing cluster managers
such as Pacemaker.
Provides a local resource manager that understands the OCF and LSB
standards, and an interface to common STONITH devices.

%package -n %{liblrm}
Summary:	Reusable cluster libraries
Group:		System/Libraries

%description -n %{liblrm}
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%package -n %{libpils}
Summary:	Reusable cluster libraries
Group:		System/Libraries

%description -n %{libpils}
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%package -n %{libplumb}
Summary:	Reusable cluster libraries
Group:		System/Libraries

%description -n %{libplumb}
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%package -n %{libplumbgpl}
Summary:	Reusable cluster libraries
Group:		System/Libraries

%description -n %{libplumbgpl}
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%package -n %{libstonith}
Summary:	Reusable cluster libraries
Group:		System/Libraries

%description -n %{libstonith}
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%package -n %{devname} 
Summary:	Headers and libraries for writing cluster managers
Group:		Development/Other
Requires:	%{liblrm} = %{version}-%{release}
Requires:	%{libpils} = %{version}-%{release}
Requires:	%{libplumb} = %{version}-%{release}
Requires:	%{libplumbgpl} = %{version}-%{release}
Requires:	%{libstonith} = %{version}-%{release}
%rename		%{name}-devel

%description -n %{devname}
Headers and shared libraries for a useful for writing cluster managers 
such as Pacemaker.

%prep
%setup -qn %{upstreamprefix}%{upstreamversion}
%apply_patches

%build
#./autogen.sh
autoreconf -fi
%configure2_5x \
	--disable-static \
	--enable-fatal-warnings=no   \
	--localstatedir=%{_var}      \
	--with-daemon-group=%{gname} \
	--with-daemon-user=%{uname}

%make

%install
%makeinstall_std

# Don't package things we wont support
rm -f %{buildroot}/%{_libdir}/stonith/plugins/stonith2/rhcs.*

%pre
%_pre_useradd %{uname} %{_var}/lib/heartbeat/cores/hacluster /bin/false
%_pre_groupadd %{gname} %{uname}

%postun
%_postun_userdel %{uname}
%_postun_groupdel %{gname}

%files
%doc AUTHORS COPYING
%{_sbindir}/cibsecret
%{_sbindir}/ha_logger
%{_sbindir}/hb_report
%{_sbindir}/lrmadmin
%{_sbindir}/meatclient
%{_sbindir}/sbd
%{_sbindir}/stonith
%{_sysconfdir}/init.d/logd

%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
%dir %{_libdir}/heartbeat/plugins/compress
%dir %{_libdir}/heartbeat/plugins/RAExec
%dir %{_libdir}/heartbeat/plugins/InterfaceMgr
%{_libdir}/heartbeat/lrmd
%{_libdir}/heartbeat/ha_logd
%{_libdir}/heartbeat/plugins/RAExec/*.so
%{_libdir}/heartbeat/plugins/InterfaceMgr/*.so
%{_libdir}/heartbeat/plugins/compress/bz2.so
%{_libdir}/heartbeat/plugins/compress/zlib.so

%dir %{_libdir}/stonith
%dir %{_libdir}/stonith/plugins
%dir %{_libdir}/stonith/plugins/stonith2
%{_datadir}/cluster-glue/ha_log.sh
%{_libdir}/stonith/plugins/external
%{_libdir}/stonith/plugins/stonith2/*.so
%{_libdir}/stonith/plugins/stonith2/*.py*
%{_libdir}/stonith/plugins/xen0-ha-dom0-stonith-helper
%dir %{_datadir}/cluster-glue
%{_datadir}/cluster-glue/ha_cf_support.sh
%{_datadir}/cluster-glue/openais_conf_support.sh
%{_datadir}/cluster-glue/utillib.sh
%{_datadir}/cluster-glue/combine-logs.pl
%dir %{_var}/lib/heartbeat
%dir %{_var}/lib/heartbeat/cores
%dir %attr (0700, root, root)		%{_var}/lib/heartbeat/cores/root
%dir %attr (0700, nobody, %{nogroup})	%{_var}/lib/heartbeat/cores/nobody
%dir %attr (0700, %{uname}, %{gname})	%{_var}/lib/heartbeat/cores/%{uname}
%doc %{_mandir}/man1/*
%doc %{_mandir}/man8/*

%files -n %{liblrm}
%{_libdir}/liblrm.so.%{major}*

%files -n %{libpils}
%{_libdir}/libpils.so.%{major}*

%files -n %{libplumb}
%{_libdir}/libplumb.so.%{major}*

%files -n %{libplumbgpl}
%{_libdir}/libplumbgpl.so.%{major}*

%files -n %{libstonith}
%{_libdir}/libstonith.so.%{maj1}*

%files -n %{devname}
%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
%dir %{_libdir}/heartbeat/plugins/test
%dir %{_datadir}/cluster-glue
%{_libdir}/lib*.so
%{_libdir}/heartbeat/ipctest
%{_libdir}/heartbeat/ipctransientclient
%{_libdir}/heartbeat/ipctransientserver
%{_libdir}/heartbeat/transient-test.sh
%{_libdir}/heartbeat/base64_md5_test
%{_libdir}/heartbeat/logtest
%{_libdir}/heartbeat/plugins/test/test.so
%{_includedir}/clplumbing
%{_includedir}/heartbeat
%{_includedir}/stonith
%{_includedir}/pils
%{_datadir}/cluster-glue/lrmtest

