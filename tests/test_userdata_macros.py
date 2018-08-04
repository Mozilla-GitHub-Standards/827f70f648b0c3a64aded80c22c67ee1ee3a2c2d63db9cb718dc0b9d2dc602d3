# coding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Tests for UserData.
"""
from collections import OrderedDict

import pytest

from laniakea.core.userdata import UserData


test_macros = OrderedDict()
test_macros["FOO"] = "FOOVAL"
test_macros["BAR"] = "BARVAL"
test_macros["BAZ"] = "BAZVAL"

userdata_test_macros = """
#!/bin/bash

# This is a sample userdata script with macros

FOO="@FOO@"
BAR=@BAR@
BAZ=some@BAZ@thing

# End
"""

userdata_test_macros_expected = """
#!/bin/bash

# This is a sample userdata script with macros

FOO="FOOVAL"
BAR=BARVAL
BAZ=someBAZVALthing

# End
"""

userdata_test_macro_export = """
#!/bin/bash

# This is a sample userdata script with macro export

@!all_macros_export@

# End
"""

userdata_test_macro_export_expected = """
#!/bin/bash

# This is a sample userdata script with macro export

export FOO="FOOVAL"
export BAR="BARVAL"
export BAZ="BAZVAL"

# End
"""

userdata_test_macro_docker = """
#!/bin/bash

# This is a sample userdata script with macro export to arguments

docker run @!all_macros_docker@ image

# End
"""

userdata_test_macro_docker_expected = """
#!/bin/bash

# This is a sample userdata script with macro export to arguments

docker run -e 'FOO=FOOVAL' -e 'BAR=BARVAL' -e 'BAZ=BAZVAL' image

# End
"""


def test_macro_replacement():
    assert UserData.handle_tags(userdata_test_macros, test_macros) == userdata_test_macros_expected

def test_macro_list_export():
    assert UserData.handle_tags(userdata_test_macro_export, test_macros) == userdata_test_macro_export_expected

def test_macro_list_docker():
    assert UserData.handle_tags(userdata_test_macro_docker, test_macros) == userdata_test_macro_docker_expected
