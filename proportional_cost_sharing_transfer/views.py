# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Frontpage(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Introduction(Page):
    """Description of the game"""
    def is_displayed(self):
        return self.subsession.round_number == 1

    pass

class Contribute(Page):
    form_model = models.Player
    form_fields = ['contribution']

    def vars_for_template(self):
        self.player.private_value = self.player.generate_private_value()


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for other participants to contribute."


class Results(Page):
    def vars_for_template(self):
        self.group.set_payoffs

        return {
            'whether_provision': self.group.provision_success,
            'whether_member': self.player.member,
            'individual_share': self.player.share*Constants.cost,
            'individual_earnings': self.player.payoff,
        }


page_sequence =[
        Frontpage,
        Introduction,
        Contribute,
        ResultsWaitPage,
        Results
    ]
