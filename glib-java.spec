Name:           glib-java
Version:        0.4.2
Release:        %mkrel 8
Epoch:          0
Summary:        Base Library for the Java-GNOME libraries 
URL:            http://java-gnome.sourceforge.net
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/glib-java/0.4/glib-java-%{version}.tar.bz2
License:        LGPL
Group:          System/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  docbook-utils
BuildRequires:  glib2-devel >= 0:2.12.4
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  java-gcj-compat-devel
BuildRequires:  java-rpmbuild
BuildRequires:  pkgconfig

%description 
Glib-java is a base framework for the Java-GNOME libraries. Allowing the use of
GNOME through Java.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Conflicts:      glib-java < 0.4.2-3

%description    devel
Development files for %{name}.

%prep
%setup -q

%build
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
export GCJ=%{gcj}
# workaround:
# libtool does not use pic_flag when compiling, so we have to force it. 
export GCJFLAGS="-O2 -fPIC" 
export CPPFLAGS="-I%{java_home}/include -I%{java_home}/include/linux"
%configure2_5x --with-jardir=%{_javadir}
# 64bit java doesn't seem to like parralell build ("Cannot create GC thread. Out of system resources"):
make

# pack up the java source
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/^lib//")
zipfile=$PWD/$jarname$jarversion-src-%{version}.zip
pushd src/java
zip -9 -r $zipfile $(find -name \*.java)
popd

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# install the src.zip and make a sym link
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/^lib//")
install -m 644 $jarname$jarversion-src-%{version}.zip $RPM_BUILD_ROOT%{_javadir}/
pushd $RPM_BUILD_ROOT%{_javadir}
ln -sf $jarname$jarversion-src-%{version}.zip $jarname$jarversion-src.zip
popd

rm -r %{buildroot}%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -p /sbin/ldconfig 
%endif
%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README 
%{_libdir}/libglibjava-*.so
%{_libdir}/libglibjni-*.so
%{_javadir}/*.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files devel
%defattr(-,root,root)
%doc doc/api
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.la
%{_libdir}/libglibjava.so
%{_libdir}/libglibjni.so
%{_libdir}/pkgconfig/*.pc
%{_javadir}/*.zip
