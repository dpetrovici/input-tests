#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Firefox Input.
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
'''

Created on Dec 22, 2010

'''

from selenium import selenium
from vars import ConnectionParameters
import unittest

import submit_suggestion_page


class SubmitSuggestion(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_remaining_character_count(self):
        """

        This testcase covers # 15029 in Litmus
        1. Verifies the remaining character count decreases
        2. Verifies that the remaining character count style changes at certain thresholds
        3. Verified that the 'Submit Feedback' button is disabled when character limit is exceeded

        """
        submit_suggestion_pg = submit_suggestion_page.SubmitSuggestionPage(self.selenium)

        submit_suggestion_pg.go_to_submit_suggestion_page()
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "250")
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertTrue(submit_suggestion_pg.is_submit_feedback_enabled)

        submit_suggestion_pg.set_feedback("a" * 199)
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "51")
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertTrue(submit_suggestion_pg.is_submit_feedback_enabled)

        submit_suggestion_pg.set_feedback("b")
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "50")
        self.assertTrue(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertTrue(submit_suggestion_pg.is_submit_feedback_enabled)

        submit_suggestion_pg.set_feedback("c" * 24)
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "26")
        self.assertTrue(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertTrue(submit_suggestion_pg.is_submit_feedback_enabled)

        submit_suggestion_pg.set_feedback("d")
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "25")
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertTrue(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertTrue(submit_suggestion_pg.is_submit_feedback_enabled)

        submit_suggestion_pg.set_feedback("e" * 25)
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "0")
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertTrue(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertTrue(submit_suggestion_pg.is_submit_feedback_enabled)

        submit_suggestion_pg.set_feedback("f")
        self.assertEqual(submit_suggestion_pg.remaining_character_count, "-1")
        self.assertFalse(submit_suggestion_pg.is_remaining_character_count_low)
        self.assertTrue(submit_suggestion_pg.is_remaining_character_count_very_low)
        self.assertFalse(submit_suggestion_pg.is_submit_feedback_enabled)

if __name__ == "__main__":
    unittest.main()
