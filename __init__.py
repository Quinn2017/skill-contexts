# Copyright 2018 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

# Author: This string of code is just a test of the @adds_context and @removes_context. It's based on an example found in GitHub, 
# but I'm not sure that it is written logically there.

from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.util.log import getLogger

__author__ = 'charles'

LOGGER = getLogger(__name__)

class GhostSkill(MycroftSkill):
    def __init__(self):
        super(GhostSkill, self).__init__(name="GhostSkill")

    @intent_handler(IntentBuilder("GhostIntent").require("GhostKeyword"))
    @adds_context("KitchenContext")
    def handle_Ghost_intent(self, message):
        self.Kitchen = False
        self.speak("It looks like there is a ghost in the kitchen", expect_response=True)

    @intent_handler(IntentBuilder("CommentIntent").require("YesKeyword").require("KitchenContext").build())
    def handle_Comment_intent(self, message):
        self.Kitchen = True
        self.speak("Did you hear anything outside?", expect_response=True)

    @intent_handler(IntentBuilder("OutsideIntent").require("QuestionKeyword").require("KitchenContext").build())
    @removes_context("KitchenContext")
    @adds_context("OutsideContext")
    def handle_Outside_intent(self, message):
        self.Outside = True
        self.speak("I heard something outside again. Did you?", expect_response=True)

    @intent_handler(IntentBuilder("ResponseIntent").require("YesKeyword").require("OutsideContext").build())
    def handle_Response_intent(self, message):
        self.Outside = True
        self.speak("There is something here.")

    def stop(self):
        pass

def create_skill():
    return GhostSkill()