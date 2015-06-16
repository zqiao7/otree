# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Ziqi Qiao'

doc = """
Proportional cost sharing with rebate, from Gailmard and Palfrey (2005) JPE
"""

class Constants:
	name_in_url = 'proportional_cost_sharing'
	players_per_group = 3
	num_rounds = 1
	cost = c(102)						#provision cost
	valuation = [c(29), c(45), c(90)]		#valuation
	payoff_if_fail = c(0)
	
    # define more constants here


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):
	# <built-in>
	subsession = models.ForeignKey(Subsession)
	# </built-in>

	provision_success = models.BooleanField()
	
	def set_payoffs(self):
		contrib = [ p.contribution for p in self.get_players() ]
		total_contrib = sum(contrib)
		self.provision_success = total_contrib > Constants.cost
		
		if self.provision_success:
			for p in self.get_players():
				p.share = p.contribution/total_contrib
				p.payoff = p.private_value - Constants.cost * p.share
		else:
			for p in self.get_players():
				p.share = 0
				p.payoff = Constants.payoff_if_fail


class Player(otree.models.BasePlayer):
	# <built-in>
	subsession = models.ForeignKey(Subsession)
	group = models.ForeignKey(Group, null = True)
	# </built-in>

	private_value = models.CurrencyField(
		null=True,
		doc="How much the player values the item, generated randomly"
	)
	
	contribution = models.PositiveIntegerField(
        min=0, max=Constants.cost,
        doc="""The amount contributed by the player""",
    )
	
	
	share = models.DecimalField(
		max_digits = 5, decimal_places = 4,
		doc="""The player's actual share of cost"""
	)
	
	def generate_private_value(self):
		return random.choice(Constants.valuation)
