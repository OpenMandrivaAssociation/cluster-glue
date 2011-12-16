%define gname haclient
%define uname hacluster
%define nogroup nobody

# When downloading directly from Mercurial, it will automatically add this prefix
# Invoking 'hg archive' wont but you can add one with: hg archive -t tgz -p "Reusable-Cluster-Components-" -r $upstreamversion $upstreamversion.tar.gz
%define upstreamprefix Reusable-Cluster-Components-glue--
%define upstreamversion glue-%{version}

# Keep around for when/if required
#global alphatag %{upstreamversion}.hg

Name:		cluster-glue
Summary:	Reusable cluster components
Version:	1.0.9
Release:	2
License:	GPLv2+ and LGPLv2+
Url:		http://linux-ha.org/wiki/Cluster_Glue
Group:		System/Libraries
Source0:	http://hg.linux-ha.org/glue/archive/%{upstreamversion}.tar.bz2
Patch0:		glue-1.0.8-gtypes.patch
# Directives to allow upgrade from combined heartbeat packages in Fedora11
Provides:	heartbeat-stonith = 3.0.0-1
Provides:	heartbeat-pils = 3.0.0-1
Obsoletes:	heartbeat-stonith < 3.0.0-1
Obsoletes:	heartbeat-pils < 3.0.0-1
Conflicts:	heartbeat < 3.0.0-1

# Build dependencies
Requires: perl-TimeDate
BuildRequires: libltdl-devel
BuildRequires: bzip2-devel
BuildRequires: glib2-devel
BuildRequires: python-devel
BuildRequires: libxml2-devel

# For documentation
BuildRequires: xsltproc docbook-style-xsl

# For additional Stonith plugins
BuildRequires: net-snmp-devel
BuildRequires: openipmi-devel
BuildRequires: curl-devel
BuildRequires: libuuid-devel

%description
A collection of common tools that are useful for writing cluster managers
such as Pacemaker.
Provides a local resource manager that understands the OCF and LSB
standards, and an interface to common STONITH devices.

%prep
%setup -q -n %{upstreamprefix}%{upstreamversion}
%patch0 -p1 -b .gtypes

%build
./autogen.sh
%configure2_5x --disable-static \
		--enable-fatal-warnings=no   \
		--localstatedir=%{_var}      \
		--with-daemon-group=%{gname} \
		--with-daemon-user=%{uname}

%make

%install
%makeinstall_std

## tree fix up
# Dont package static libs
find %{buildroot} -name '*.la' -exec rm {} \;

# Don't package things we wont support
rm -f %{buildroot}/%{_libdir}/stonith/plugins/stonith2/rhcs.*

%pre
%_pre_useradd %{uname} %{_var}/lib/heartbeat/cores/hacluster /bin/false
%_pre_groupadd %{gname} %{uname}

%postun
%_postun_userdel %{uname}
%_postun_groupdel %{gname}

%files
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
%dir %{_libdir}/heartbeat/plugins/RAExec
%dir %{_libdir}/heartbeat/plugins/InterfaceMgr
%{_libdir}/heartbeat/lrmd
%{_libdir}/heartbeat/ha_logd
%{_libdir}/heartbeat/plugins/RAExec/*.so
%{_libdir}/heartbeat/plugins/InterfaceMgr/*.so

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

#doc %{_datadir}/doc/cluster-glue/stonith
%doc %{_mandir}/man1/*
%doc %{_mandir}/man8/*
%doc AUTHORS
%doc COPYING

#---------------------------------------------------------
%define lrmmajor 2
%define liblrm %mklibname lrm %lrmmajor

%package -n %liblrm
Summary:	Reusable cluster libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %liblrm
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%files -n %liblrm
%{_libdir}/liblrm.so.%{lrmmajor}
%{_libdir}/liblrm.so.%{lrmmajor}.*

#---------------------------------------------------------
%define pilsmajor 2
%define libpils %mklibname pils %pilsmajor

%package -n %libpils
Summary:	Reusable cluster libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %libpils
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%files -n %libpils
%{_libdir}/libpils.so.%{pilsmajor}
%{_libdir}/libpils.so.%{pilsmajor}.*

#---------------------------------------------------------
%define plumbmajor 2
%define libplumb %mklibname plumb %plumbmajor

%package -n %libplumb
Summary:	Reusable cluster libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %libplumb
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%files -n %libplumb
%{_libdir}/libplumb.so.%{plumbmajor}
%{_libdir}/libplumb.so.%{plumbmajor}.*

#---------------------------------------------------------
%define plumbgplmajor 2
%define libplumbgpl %mklibname plumbgpl %plumbgplmajor

%package -n %libplumbgpl
Summary:	Reusable cluster libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %libplumbgpl
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%files -n %libplumbgpl
%{_libdir}/libplumbgpl.so.%{plumbgplmajor}
%{_libdir}/libplumbgpl.so.%{plumbgplmajor}.*

#---------------------------------------------------------
%define stonithmajor 1
%define libstonith %mklibname stonith %stonithmajor

%package -n %libstonith
Summary:	Reusable cluster libraries
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{_lib}heartbeat-stonith1 < 3.0.0-1

%description -n %libstonith
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%files -n %libstonith
%{_libdir}/libstonith.so.%{stonithmajor}
%{_libdir}/libstonith.so.%{stonithmajor}.*

#---------------------------------------------------------

%package devel 
Summary: Headers and libraries for writing cluster managers
Group: Development/Other
Requires: %{liblrm} = %{version}-%{release}
Requires: %{libpils} = %{version}-%{release}
Requires: %{libplumb} = %{version}-%{release}
Requires: %{libplumbgpl} = %{version}-%{release}
Requires: %{libstonith} = %{version}-%{release}
Obsoletes: %{_lib}heartbeat1-devel < 3.0.0-1
Obsoletes: %{_lib}heartbeat-pils1-devel < 3.0.0-1
Obsoletes: %{_lib}heartbeat-stonith1-devel < 3.0.0-1

%description devel
Headers and shared libraries for a useful for writing cluster managers 
such as Pacemaker.

%files devel
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
%{_includedir}/clplumbing
%{_includedir}/heartbeat
%{_includedir}/stonith
%{_includedir}/pils
%{_datadir}/cluster-glue/lrmtest
%{_libdir}/heartbeat/plugins/test/test.so
