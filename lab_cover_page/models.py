# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = ''

doc = """
This is a cover page for lab sessions. 
"""

class Constants:
    name_in_url = 'lab_cover_page'
    players_per_group = None
    num_rounds = 1

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>


