# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady —
# :Created:   dom 4 giu 2023, 17:38:28
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2023 Lele Gaifax
#

# List of Python versions to test against, keep it in sync with flake.nix
SNAKES = 310 311
POTIONS = 14 20

.PHONY: test

define test-snake
test:: test-python$(1)-sqlalchemy$(2)

.PHONY: test-python$(1)-sqlalchemy$(2)
test-python$(1)-sqlalchemy$(2):
	nix develop '.#test-python$(1)-sqlalchemy$(2)' -c just check
endef

$(foreach snake,$(SNAKES),$(foreach potion,$(POTIONS),$(eval $(call test-snake,$(snake),$(potion)))))
