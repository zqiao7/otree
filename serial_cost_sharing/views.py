# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

	
	
class  Contribute(Page):

    form_model = models.Player
    form_fields = ['contribution']




class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		self.group.set_payoffs()
		
	def body_text(self):
		return "Waiting for other participants to contribute."


class Results(Page):

	def vars_for_template(self):

		return {
            'whether_provision': self.Group.provision_success,
            'individual_earnings': self.Player.payoff,
        }


page_sequence =[
        Contribute,
        ResultsWaitPage,
        Results
    ]
