Summary:	X Window System Smalltalk interpreter
Summary(pl):	Interpreter Smalltalka dla X Window System
Name:		squeak
Version:	3.6
Release:	1
%define	vmver 3.4-1
License:	partially GPL
Group:		Development/Languages
Source0:	ftp://st.cs.uiuc.edu/Smalltalk/Squeak/%{version}/unix-linux/Squeak-%{vmver}.src.tar.gz
# Source0-md5:	780af1cf1cdc8d44c1ce30a527bdd508
Source1:	ftp://st.cs.uiuc.edu/Smalltalk/Squeak/3.6/Squeak3.6-5429-full.zip
# Source1-md5:	9a35fa39f2338d26a721564472d4d933
Source2:	ftp://st.cs.uiuc.edu/Smalltalk/Squeak/%{version}/SqueakV3.sources.gz
# Sources2-md5:	03791c6e87f032230d55249dcc9ac3c9
Source4:	%{name}-install
URL:		http://www.squeak.org/
BuildRequires:	XFree86-devel
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Squeak is an open, highly-portable Smalltalk-80 implementation whose
virtual machine is written entirely in Smalltalk, making it easy to
debug, analyze, and change. To achieve practical performance, a
translator produces an equivalent C program whose performance is
comparable to commercial Smalltalks.

%description -l pl
Squeak jest otwart±, przeno¶n± implementacj± jêzyka Smalltalk-80, z
maszyn± wirtualn± napisan± ca³kowicie w Smalltalku, dziêki czemu daje
siê ona ³atwo poprawiaæ, analizowaæ i zmieniaæ. W celu osi±gniêcia
praktycznej wydajno¶ci, translator produkuje odpowiedni program w C,
którego efektywno¶æ jest porównywalna z komercyjnymi Smalltalkami.

%package extras
Summary:	extra libraries for Squeak 2.X
Summary(pl):	dodatkowe biblioteki dla Squeaka 2.X
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description extras
A set of extra shared-libraries for Squeak: Squeak3D and
SoundCodecPrisms

%description extras -l pl
Zestaw dodatkowych bibliotek dla Squeaka: Squeak3D oraz
SoundCodecPrisms

%package -n mozilla-plugin-squeak
Summary:	Plugin to run Squeak in your browser
Summary(pl):	Wtyczka do uruchamiania Squeaka w przegl±darce
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n mozilla-plugin-squeak
Plugin to run Squeak in your browser.

%description -n mozilla-plugin-squeak -l pl
Wtyczka do uruchamiania Squeaka w przegl±darce.

%prep
%setup -q -c -a1

%build
cd Squeak-%{vmver}
cd platforms/unix/config
./mkacinc > acplugins.m4
%{__aclocal}
%{__autoconf}
cd ../../..
mkdir bld
cd bld
../platforms/unix/config/%{configure}
cat <<EOF >disabledPlugins.c
typedef struct {
  char *pluginName;
  char *primitiveName;
  void *primitiveAddress;
} sqExport;
EOF
%{__make} 
unzip %{SOURCE1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir}/squeak,%{_bindir}}

cd Squeak-%{vmver}/bld

%{__make} install \
	ROOT=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/squeak
install Squeak3.6-5429-full.changes $RPM_BUILD_ROOT%{_datadir}/squeak/squeak.changes
install Squeak3.6-5429-full.image $RPM_BUILD_ROOT%{_datadir}/squeak/squeak.image

gzip -d $RPM_BUILD_ROOT%{_datadir}/squeak/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post	extras -p /sbin/ldconfig
%postun extras -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/squeak
%dir %{_libdir}/squeak/%{vmver}
%attr(755,root,root) %{_libdir}/squeak/%{vmver}/squeak
%dir %{_datadir}/squeak
%attr(755,root,root) %{_datadir}/squeak/squeak.changes
%attr(755,root,root) %{_datadir}/squeak/squeak.image
# ??? duplicates
%{_datadir}/squeak
%{_mandir}/man1/squeak.1*

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/squeak/%{vmver}/*Plugin

%files -n mozilla-plugin-squeak
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/squeak/%{vmver}/npsqueakrun
%attr(755,root,root) %{_libdir}/squeak/npsqueakregister
%attr(755,root,root) %{_libdir}/squeak/%{vmver}/npsqueak.so
