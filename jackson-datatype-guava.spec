%global pkg_name jackson-datatype-guava
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}
Name:          %{?scl_prefix}jackson-datatype-guava
Version:       2.5.0
Release:       2.1%{?dist}
Summary:       Add-on module for Jackson JSON processor which handles Guava data-types
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonModuleGuava
Source0:       https://github.com/FasterXML/jackson-datatype-guava/archive/%{pkg_name}-%{version}.tar.gz

BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires: %{?scl_prefix}mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava) >= 15.0
# test deps
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)

BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix_maven}maven-enforcer-plugin
BuildRequires: %{?scl_prefix_maven}maven-plugin-build-helper
BuildRequires: %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires: %{?scl_prefix_maven}maven-site-plugin
BuildRequires: %{?scl_prefix_maven}maven-surefire-provider-junit

BuildArch:     noarch

%description
Add-on datatype-support module for Jackson that handles
Guava types (currently mostly just collection ones).

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

sed -i 's/\r//' src/main/resources/META-INF/LICENSE
cp -p src/main/resources/META-INF/LICENSE .

%pom_xpath_remove "pom:properties/pom:osgi.import"
%pom_xpath_inject "pom:properties" "
    <osgi.import>
com.google.common.collect,
com.google.common.base,
com.google.common.cache,
com.google.common.hash,
com.google.common.net,
com.fasterxml.jackson.core,
com.fasterxml.jackson.core.util,
com.fasterxml.jackson.databind,
com.fasterxml.jackson.databind.deser,
com.fasterxml.jackson.databind.deser.std,
com.fasterxml.jackson.databind.introspect,
com.fasterxml.jackson.databind.jsonFormatVisitors,
com.fasterxml.jackson.databind.jsontype,
com.fasterxml.jackson.databind.ser,
com.fasterxml.jackson.databind.ser.std,
com.fasterxml.jackson.databind.ser.impl,
com.fasterxml.jackson.databind.type,
com.fasterxml.jackson.databind.util
</osgi.import>"


%mvn_file : %{pkg_name}

%pom_remove_parent

%pom_xpath_inject "pom:build/pom:plugins" '
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <version>1.0.0</version>
          <configuration>
            <instructions>
              <_nouses>true</_nouses>
              <_removeheaders>Include-Resource,JAVA_1_3_HOME,JAVA_1_4_HOME,JAVA_1_5_HOME,JAVA_1_6_HOME,JAVA_1_7_HOME</_removeheaders>
              <_versionpolicy>${osgi.versionpolicy}</_versionpolicy>
              <Bundle-Name>${project.name}</Bundle-Name>
              <Bundle-SymbolicName>${project.groupId}.${project.artifactId}</Bundle-SymbolicName>
              <Bundle-Description>${project.description}</Bundle-Description>
              <Export-Package>${osgi.export}</Export-Package>
              <Private-Package>${osgi.private}</Private-Package>
              <Import-Package>${osgi.import}</Import-Package>
              <DynamicImport-Package>${osgi.dynamicImport}</DynamicImport-Package>
              <Bundle-DocURL>${project.url}</Bundle-DocURL>
              <Bundle-RequiredExecutionEnvironment>${osgi.requiredExecutionEnvironment}</Bundle-RequiredExecutionEnvironment>

              <Implementation-Build-Date>${maven.build.timestamp}</Implementation-Build-Date>
              <X-Compile-Source-JDK>${javac.src.version}</X-Compile-Source-JDK>
              <X-Compile-Target-JDK>${javac.target.version}</X-Compile-Target-JDK>

              <Implementation-Title>${project.name}</Implementation-Title>
              <Implementation-Version>${project.version}</Implementation-Version>
              <Implementation-Vendor-Id>${project.groupId}</Implementation-Vendor-Id>
              <Implementation-Vendor>${project.organization.name}</Implementation-Vendor>

              <Specification-Title>${project.name}</Specification-Title>
              <Specification-Version>${project.version}</Specification-Version>
              <Specification-Vendor>${project.organization.name}</Specification-Vendor>
            </instructions>
          </configuration>
        </plugin>'

%pom_xpath_inject "pom:properties" '
<osgi.versionpolicy>${range;[===,=+);${@}}</osgi.versionpolicy>'

%pom_add_dep "junit:junit"

# Avoid using the replacer-plugin
%pom_remove_plugin com.google.code.maven-replacer-plugin:replacer

file=`find -name PackageVersion.java.in`
gid=`grep "<groupId>" pom.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/'`
aid=`grep "<artifactId>" pom.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/'`
v=`grep "<version>" pom.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/'`
pkg=`echo ${file} | cut -d/ -f5- | rev | cut -d/ -f2- | rev | tr '/' '\.'`

sed -i "s/@projectversion@/${v}/
        s/@projectgroupid@/${gid}/
        s/@package@/${pkg}/
        s/@projectartifactid@/${aid}/" ${file}

cp ${file} ${file%.in}

%{?scl:EOF}

%build

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}

%mvn_build

%{?scl:EOF}

%install

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install

%{?scl:EOF}

%files -f .mfiles
%doc README.md release-notes/* LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Jul 02 2015 Roland Grunberg <rgrunber@redhat.com> - 2.5.0-2.1
- SCL-ize.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Wed Dec 17 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Sat Dec 07 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm
