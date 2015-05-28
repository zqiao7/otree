# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

import numpy as np

# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""

class Constants:
	name_in_url = 'serial_cost_sharing'
	players_per_group = 3
	num_rounds = 1
	cost = 102						#provision cost
	valuation = [29, 45, 90]		#valuation
	payoff_if_fail = c(0)
	
	offer_choices = [0, 1/2, 1/3]
	offer_choices_count = len(offer_choices)

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    
	def before_session_starts(self):
		# randomly assign values
		for g in self.get_players():
			g.value = random.choice(constants.valuation,1)


class Group(otree.models.BaseGroup):
    # <built-in>
	subsession = models.ForeignKey(Subsession)
    # </built-in>

	
	valuation = models.CurrencyField()
	amount_offered = models.CurrencyField(choices=Constants.offer_choices)
	#total_contribution = models.CurrencyField()
	#individual_share = models.CurrencyField()
	provision_success = models.BooleanField()
	individual_share = models.BooleanField()
	
	def set_payoffs(self):
		#p1, p2, p3 = self.get_players()
		
		contrib = [p.contribution for p in self.get_players()]
		self.provision_success = min(contrib) > 0 or min(contrib.remove(min.contrib)) == 1/2
		if self.provision_success:
			if min(contrib)>0:
				num_of_members = 3
			else:
				num_of_members = 2
			
		
		for p in self.get_players():
			p.valuation =  p.value
			
			if self.provision_success:
				p.individual_share = p.valuation > min(constants.valuation)
				if p.individual_share:
					p.payoff = p.valuation - constants.cost/num_of_members
				else:
					p.payoff = 0
			else:
				p.payoff = 0


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    
	# def other_player(self):
        # """Returns other player in group. Only valid for 2-player groups."""
        # return self.get_others_in_group()[0]

    # # example field
    # my_field = models.CurrencyField(
        # min=c(0),
        # max=c(10),
        # doc="""
        # Description of this field, for documentation
        # """
    # )


    # def role(self):
        # # you can make this depend of self.id_in_group
        # return ''
