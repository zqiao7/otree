# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants 
#from .models import Player
import random

class Introduction(Page):

    """Description of the game: How to play and returns expected"""
    pass
	
class  Contribute(Page):
 
	form_model = models.Player
	form_fields = ['contribution']
	
	def vars_for_template(self):
		#if self.player.private_value is None:
			self.player.private_value = self.player.generate_private_value()
			
	#auto_submit_values = {'contribution': random.randint(0, Player.private_value)}




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
            'individual_share': self.player.share*Constants.cost,
            'individual_earnings': self.player.payoff,
        }


page_sequence =[
		Introduction,
        Contribute,
        ResultsWaitPage,
        Results
    ]
