# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

import numpy

# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""

class Constants:
	name_in_url = 'optimal_cost_sharing'
	players_per_group = 3
	num_rounds = 5
	cost = c(102)						#provision cost
	valuation = [c(29), c(45), c(90)]		#valuation
	payoff_if_fail = c(0)
	
	offer_value = {'Low':c(29),'Median':c(45),'High':c(90)}
	offer_choices = ['Low', 'Median', 'High']
	
	# payment scheme
	t_L_LL = c(0)
	t_L_LM = c(0)
	t_M_LL = c(0)

	t_L_MM = c(28)
	t_M_LM = c(37)

	t_M_MM = c(34)

	t_L_LH = c(28)
	t_H_LL = c(46)

	t_L_MH = c(28)
	t_M_LH = c(29)
	t_H_LM = c(45)

	t_M_MH = c(32)
	t_H_MM = c(40)

	t_L_HH = c(28)
	t_H_LH = c(37)

	t_M_HH = c(28)
	t_H_MH = c(37)

	t_H_HH = c(34)
	
	payment = {
			'Low':numpy.array(
							[[t_L_HH,t_L_MH,t_L_MM],
							 [t_L_LH,t_L_LM,999999],
							 [t_L_LL,999999,999999]]
						    ),
			'Median':numpy.array(
							[[t_M_HH,t_M_MH,t_M_MM],
							 [t_M_LH,t_M_LM,999999],
							 [t_M_LL,999999,999999]]
						    ),
			'High':numpy.array(
							[[t_H_HH,t_H_MH,t_H_MM],
							 [t_H_LH,t_H_LM,999999],
							 [t_H_LL,999999,999999]]
						    )
		    }

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    pass

class Group(otree.models.BaseGroup):
    # <built-in>
	subsession = models.ForeignKey(Subsession)
    # </built-in>
    
	provision_success = models.BooleanField()
	
	def set_payoffs(self):
		
		contrib = [ Constants.offer_value[p.contribution] for p in self.get_players()]
		self.provision_success = (
			sum(contrib) >= Constants.cost + c(2)
		)
		
		for p in self.get_players():
				
			if self.provision_success:
				other_bids = [ x.contribution for x in self.get_players() 
							if x!= p]
				num_L = other_bids.count('Low')
				num_M = other_bids.count('Median')
				p.share = Constants.payment[p.contribution][num_L,num_M]
				p.payoff = Constants.offer_value[p.contribution]-p.share
			else:
				p.share = 0
				p.payoff = 0



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
		doc="""The player's choice of report.""",
		widget=widgets.RadioSelect()
	)
	
	
	share = models.CurrencyField(
		null=True,
		doc="""The player's actual cost."""
	)
	
	def generate_private_value(self):
		return random.choice(Constants.valuation)
	
