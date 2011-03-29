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
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bob Silverberg <bob.silverberg@gmail.com>
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
Created on Mar 29, 2011
'''

import submit_feedback_page

class SubmitFeedbackPage(submit_feedback_page.SubmitFeedbackPage):

    _page_title = u'Submit Feedback :: Firefox Input'

    def is_submit_feedback_enabled(self):
        return self.selenium.is_element_present("css=a[data-waittext='Submitting Feedback']") 
        + self.selenium.is_element_not_present("css=a[data-waittext='Submitting Feedback'][class='disabled']")

    def is_submit_feedback_disabled(self):
        return self.selenium.is_element_present("css=a[data-waittext='Submitting Feedback']") 
        + self.selenium.is_element_present("css=a[data-waittext='Submitting Feedback'][class='disabled']")

    @property
    def is_remaining_character_count_low(self):
        try:
            return self.selenium.get_attribute(self._remaining_character_count_locator + "@class") == "count low"
        except:
            return False

    @property
    def is_remaining_character_count_very_low(self):
        try:
            return self.selenium.get_attribute(self._remaining_character_count_locator + "@class") == "count verylow"
        except:
            return False
    
    def submit_feedback(self):
        self.selenium.click(self._submit_feedback_locator)
