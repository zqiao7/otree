# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

import numpy as np
from fractions import Fraction
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""

class Constants:
	name_in_url = 'serial_cost_sharing'
	players_per_group = 3
	num_rounds = 1
	cost = c(102)						#provision cost
	valuation = [c(29), c(45), c(90)]		#valuation
	payoff_if_excluded = c(0)
	payoff_if_fail = c(0)
	
	
	offer_choices = ['0', '1/3', '1/2']



class Subsession(otree.models.BaseSubsession):
    
	pass


class Group(otree.models.BaseGroup):
    # <built-in>
	subsession = models.ForeignKey(Subsession)
    # </built-in>

	
	provision_success = models.BooleanField()
	num_of_members = models.CurrencyField()
	
	def set_payoffs(self):
		
		contrib = [float(Fraction(p.contribution)) for p in self.get_players()]
		contrib_1 = [float(Fraction(p.contribution)) for p in self.get_players()]
		contrib_1.remove(min(contrib_1))
		self.provision_success = (
			min(contrib) > 0 or 
			min(contrib_1) == 1/2
		)
		
		if self.provision_success:
			if min(contrib) > 0:
				num_of_members = 3
			else:
				num_of_members = 2
		else:
			num_of_members = 0
		
		for p in self.get_players():
			
			if self.provision_success:
				p.member = Fraction(p.contribution) > 0
				if p.member:
					p.share = Constants.offer_choices[::-1][num_of_members-2]
					p.payoff = p.private_value - Constants.cost/num_of_members
				else:
					p.payoff = Constants.payoff_if_excluded
					p.share = Constants.offer_choices[0]
			else:
				p.member = False
				p.payoff = Constants.payoff_if_fail
				p.share = Constants.offer_choices[0]


class Player(otree.models.BasePlayer):
    # <built-in>
	subsession = models.ForeignKey(Subsession)
	group = models.ForeignKey(Group, null = True)
	# <built-in>
	
	private_value = models.CurrencyField(
		null=True,
		doc="How much the player values the item, generated randomly"
	)
	
	contribution = models.CharField(
		choices = Constants.offer_choices,
		doc="""The player's choice""",
		widget=widgets.RadioSelect()
	)
	
	member = models.BooleanField()
	
	share = models.CharField(
		choices = Constants.offer_choices,
		doc="""The player's actual share of cost"""
	)
	
	def generate_private_value(self):
		return random.choice(Constants.valuation)
	
