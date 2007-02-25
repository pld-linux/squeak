%define	vmver 3.4-1
Summary:	X Window System Smalltalk interpreter
Summary(pl.UTF-8):	Interpreter Smalltalka dla X Window System
Name:		squeak
Version:	3.6
Release:	2
License:	partially GPL
Group:		Development/Languages
Source0:	ftp://st.cs.uiuc.edu/Smalltalk/Squeak/%{version}/unix-linux/Squeak-%{vmver}.src.tar.gz
# Source0-md5:	780af1cf1cdc8d44c1ce30a527bdd508
Source1:	ftp://st.cs.uiuc.edu/Smalltalk/Squeak/%{version}/Squeak3.6-5429-full.zip
# Source1-md5:	9a35fa39f2338d26a721564472d4d933
Source2:	ftp://st.cs.uiuc.edu/Smalltalk/Squeak/%{version}/SqueakV3.sources.gz
# Sources2-md5:	03791c6e87f032230d55249dcc9ac3c9
Source4:	%{name}-install
Patch0:		%{name}-lvalue-assignment.patch
URL:		http://www.squeak.org/
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	unzip
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Squeak is an open, highly-portable Smalltalk-80 implementation whose
virtual machine is written entirely in Smalltalk, making it easy to
debug, analyze, and change. To achieve practical performance, a
translator produces an equivalent C program whose performance is
comparable to commercial Smalltalks.

%description -l pl.UTF-8
Squeak jest otwartą, przenośną implementacją języka Smalltalk-80, z
maszyną wirtualną napisaną całkowicie w Smalltalku, dzięki czemu daje
się ona łatwo poprawiać, analizować i zmieniać. W celu osiągnięcia
praktycznej wydajności, translator produkuje odpowiedni program w C,
którego efektywność jest porównywalna z komercyjnymi Smalltalkami.

%package extras
Summary:	extra libraries for Squeak 2.X
Summary(pl.UTF-8):	dodatkowe biblioteki dla Squeaka 2.X
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description extras
A set of extra shared-libraries for Squeak: Squeak3D and
SoundCodecPrisms

%description extras -l pl.UTF-8
Zestaw dodatkowych bibliotek dla Squeaka: Squeak3D oraz
SoundCodecPrisms

%package -n mozilla-plugin-squeak
Summary:	Plugin to run Squeak in your browser
Summary(pl.UTF-8):	Wtyczka do uruchamiania Squeaka w przeglądarce
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n mozilla-plugin-squeak
Plugin to run Squeak in your browser.

%description -n mozilla-plugin-squeak -l pl.UTF-8
Wtyczka do uruchamiania Squeaka w przeglądarce.

%prep
%setup -q -c -a1
%patch0 -p1

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
