mod_mod_inseop.la: mod_mod_inseop.slo
	$(SH_LINK) -rpath $(libexecdir) -module -avoid-version  mod_mod_inseop.lo
DISTCLEAN_TARGETS = modules.mk
shared =  mod_mod_inseop.la
