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

author = 'Ziqi Qiao'

doc = """
Proportional cost sharing with reservation and transfer
"""

class Constants:
    name_in_url = 'proportional_cost_sharing_transfer'
    players_per_group = 3
    num_rounds = 1
    cost = c(102)
    valuation = [c(29), c(45), c(90)]
    payoff_if_fail = c(0)
    reserve = 21
    transfer = 1

    offer_choices = [str(x) for x in np.arange(103)]

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    def before_session_starts(self):
        player = []

        for g in self.get_groups():
            player = player + g.get_players()

        random.shuffle(player)
        
        for g in self.get_groups():
            g_player = player[0:Constants.players_per_group]
            g.set_players(g_player)
            player = list(set(player) - set(g_player))


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    provision_success = models.BooleanField()

    def set_payoffs(self):
        contrib = [ int(p.contribution) for p in self.get_players() ]
        contrib_1 = [ x for x in contrib if x >= Constants.reserve ]
        total_contrib = sum(contrib_1)
        self.provision_success = total_contrib > Constants.cost
        
        if self.provision_success:
            for p in self.get_players():
                p.member = int(p.contribution) >= Constants.reserve
                p.share = int(p.member)*int(p.contribution)/total_contrib
                lower = int(p.member)*sum(x > int(p.contribution) for x in contrib_1)
                higher = int(p.member)*sum(x < int(p.contribution) for x in contrib_1)
                p.transfer = (lower-higher)*Constants.transfer
                p.payoff = int(p.member)*(p.private_value - Constants.cost*p.share - p.transfer) + (1 - int(p.member))*Constants.payoff_if_fail
        else:
            for p in self.get_players():
                p.member = 1>2
                p.share = 0
                p.payoff = Constants.payoff_if_fail


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    private_value = models.CurrencyField(
        null=True,
        doc="How much the player values the item, generate randomly"
    )

    contribution = models.CharField(
        choices = Constants.offer_choices,
        doc = """Player's choice of contribution """,
        widget = widgets.Select()
    )

    member = models.BooleanField()

    share = models.DecimalField(
        max_digits = 5, decimal_places = 4,
        doc="""The player's actual share of cost"""
    )

    transfer = models.IntegerField()

    def generate_private_value(self):
        return random.choice(Constants.valuation)
