#
# Makefile - build wrapper for awscli on CentPOS 7
#
#	git clone RHEL 7 SRPM building tools from
#	https://github.com/nkadel/[package] into designated
#	AWSCLIPKGS below
#
#	Set up local 

# Rely on local nginx service poingint to file://$(PWD)/awsclirepo
#REPOBASE = http://localhost
REPOBASE = file://$(PWD)

# Placeholder RPMs for python2-foo packages to include python-foo
EPELPKGS+=python-fixtures-srpm

# Build python3 versions of packages
#EPELPKGS+=python-colorama-srpm
EPELPKGS+=python-d2to1-srpm
EPELPKGS+=python-jmespath-srpm
EPELPKGS+=python-boto-srpm
#EPELPKGS+=python-boto3-srpm
EPELPKGS+=python-botocore-srpm
EPELPKGS+=python-s3transfer-srpm
EPELPKGS+=python-unittest2-srpm

# Actually compilable with centos+epel-7-x86_64 alone
EPELPKGS+=python-awscli-srpm

AWSCLIPKGS+=python-rsa-srpm

AWSCLIPKGS+=python-pbr-srpm

# dependencies
AWSCLIPKGS+=python-linecache2-srpm

REPOS+=awsclirepo/el/7
REPOS+=awsclirepo/el/8
REPOS+=awsclirepo/el/9

REPODIRS := $(patsubst %,%/x86_64/repodata,$(REPOS)) $(patsubst %,%/SRPMS/repodata,$(REPOS))

# No local dependencies at build time
CFGS+=awsclirepo-7-x86_64.cfg
CFGS+=awsclirepo-8-x86_64.cfg
CFGS+=awsclirepo-9-x86_64.cfg

# Link from /etc/mock
MOCKCFGS+=centos+epel-7-x86_64.cfg
MOCKCFGS+=centos-stream+epel-8-x86_64.cfg
MOCKCFGS+=centos-stream+epel-9-x86_64.cfg

all:: install
install:: $(CFGS) $(MOCKCFGS)
install:: $(REPODIRS)
install:: $(EPELPKGS)
install:: $(AWSCLIPKGS)

build install clean getsrc build:: FORCE
	@for name in $(EPELPKGS) $(AWSCLIPKGS); do \
	     (cd $$name; $(MAKE) $(MFLAGS) $@); \
	done  

# It is sometimes useful to build up all the more independent EPEL packages first
epel:: $(EPELPKGS)

# Dependencies for order sensitivity
#python-awscli-srpm::
#
#python-botocore-srpm:: python-jmespath-srpm
#
#python-linecache2-srpm:: python-fixtures-srpm
#python-linecache2-srpm:: python-unittest2-srpm

# Actually build in directories
$(EPELPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

$(AWSCLIPKGS):: FORCE
	(cd $@; $(MAKE) $(MLAGS) install)

repos: $(REPOS) $(REPODIRS)
$(REPOS):
	install -d -m 755 $@

.PHONY: $(REPODIRS)
$(REPODIRS): $(REPOS)
	@install -d -m 755 `dirname $@`
	/usr/bin/createrepo_c `dirname $@`


.PHONY: cfg cfgs
cfg cfgs:: $(CFGS) $(MOCKCFGS)

$(MOCKCFGS)::
	@echo Generating $@ from /etc/mock/$@
	@echo "include('/etc/mock/$@')" | tee $@

awsclirepo-7-x86_64.cfg: /etc/mock/centos+epel-7-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" | tee $@
	@echo | tee -a $@
	@echo "config_opts['root'] = 'awsclirepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['yum.conf'] += \"\"\"" | tee -a $@
	@echo '[awsclirepo]' | tee -a $@
	@echo 'name=awsclirepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awsclirepo/el/7/x86_64/' | tee -a $@
	@echo 'failovermethod=priority' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '#cost=2000' | tee -a $@
	@echo '"""' | tee -a $@

awsclirepo-8-x86_64.cfg: /etc/mock/centos-stream+epel-8-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" > $@
	@echo "config_opts['root'] = 'awsclirepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awsclirepo]' | tee -a $@
	@echo 'name=awsclirepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awsclirepo/el/8/x86_64/' | tee -a $@
	@echo 'failovermethod=priority' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '#cost=2000' | tee -a $@
	@echo '"""' | tee -a $@

awsclirepo-9-x86_64.cfg: /etc/mock/centos-stream+epel-9-x86_64.cfg
	@echo Generating $@ from $?
	@echo "include('$?')" > $@
	@echo "config_opts['root'] = 'awsclirepo-{{ releasever }}-{{ target_arch }}'" | tee -a $@
	@echo "config_opts['dnf.conf'] += \"\"\"" | tee -a $@
	@echo '[awsclirepo]' | tee -a $@
	@echo 'name=awsclirepo' | tee -a $@
	@echo 'enabled=1' | tee -a $@
	@echo 'baseurl=$(REPOBASE)/awsclirepo/el/9/x86_64/' | tee -a $@
	@echo 'failovermethod=priority' | tee -a $@
	@echo 'skip_if_unavailable=False' | tee -a $@
	@echo 'metadata_expire=1' | tee -a $@
	@echo 'gpgcheck=0' | tee -a $@
	@echo '#cost=2000' | tee -a $@
	@echo '"""' | tee -a $@

repo: awsclirepo.repo
awsclirepo.repo:: Makefile awsclirepo.repo.in
	if [ -s /etc/fedora-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/fedora/|g" > $@; \
	elif [ -s /etc/redhat-release ]; then \
		cat $@.in | \
			sed "s|@REPOBASEDIR@/|$(PWD)/|g" | \
			sed "s|/@RELEASEDIR@/|/el/|g" > $@; \
	else \
		echo Error: unknown release, check /etc/*-release; \
		exit 1; \
	fi

awsclirepo.repo:: FORCE
	cmp -s /etc/yum.repos.d/$@ $@       


nginx:: nginx/default.d/awsclirepo.conf

nginx/default.d/awsclirepo.conf:: FORCE nginx/default.d/awsclirepo.conf.in
	cat $@.in | \
		sed "s|@REPOBASEDIR@;|$(PWD)/;|g" | tee $@;

nginx/default.d/awsclirepo.conf:: FORCE
	cmp -s $@ /etc/$@ || \
	    diff -u $@ /etc/$@

clean::
	find . -name \*~ -exec rm -f {} \;
	rm -f *.cfg
	rm -f *.out
	rm -f nginx/default.d/*.conf
	@for name in $(AWSCLIPKGS); do \
	    $(MAKE) -C $$name clean; \
	done

distclean:
	rm -rf $(REPOS)

maintainer-clean:
	rm -rf $(AWSCLIPKGS)

FORCE::
