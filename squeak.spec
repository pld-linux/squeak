Summary:	X Window System Smalltalk interpreter
Summary(pl):	Interpreter Smalltalka dla X Window System
Name:		squeak
Version:	2.6
Release:	1
License:	partially GPL
Group:		Development/Languages
Source0:	http://www-sor.inria.fr/~piumarta/squeak/unix/release/Squeak%{version}-src.tar.gz
# Source0-md5:	7e0728d338d6464b9689ef69eade1c3f
Source1:	http://www-sor.inria.fr/~piumarta/squeak/unix/release/Squeak%{version}.image.gz
# Source1-md5:	eb2cfe3f6eb18df2fb49f8f66a6e6a5c
Source2:	http://www-sor.inria.fr/~piumarta/squeak/unix/release/Squeak%{version}.changes.gz
# Source2-md5:	46de633f17dee23b0c06d5ac62473c77
Source3:	http://www-sor.inria.fr/~piumarta/squeak/unix/release/SqueakV2.sources.gz
# Source3-md5:	03791c6e87f032230d55249dcc9ac3c9
Source4:	%{name}-install
URL:		http://www.squeak.org/
BuildRequires:	XFree86-devel
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
Requires:	%{name}

%description extras
A set of extra shared-libraries for Squeak: Squeak3D and
SoundCodecPrisms

%description extras -l pl
Zestaw dodatkowych bibliotek dla Squeaka: Squeak3D oraz
SoundCodecPrisms

%prep
%setup -q -c

%build
%{__make} -C %{_misc_version} \
	VMBUILD=bin \
	TARGET=bin \
	CCFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir}/squeak,%{_bindir}}

cd %{_misc_version}
install bin/SqueakVM-2.4c-bin $RPM_BUILD_ROOT%{_bindir}/squeak
install util/{sq,qs}cat $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/squeak-install
install bin/*.so $RPM_BUILD_ROOT%{_libdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/squeak/squeak.image.gz
install %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/squeak/squeak.changes.gz
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/squeak
gzip -d $RPM_BUILD_ROOT%{_datadir}/squeak/*.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post	extras -p /sbin/ldconfig
%postun	extras -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/squeak*
%attr(755,root,root) %{_bindir}/sqcat
%attr(755,root,root) %{_bindir}/qscat
%{_datadir}/squeak

%files extras
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/Squeak3D.so
%attr(755,root,root) %{_libdir}/SoundCodecPrims.so
