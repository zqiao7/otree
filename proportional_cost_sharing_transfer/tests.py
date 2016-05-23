# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants
from .models import Player


class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):
        self.submit(views.Frontpage)
        self.submit(views.Introduction)
        self.submit(
            views.Contribute, {"contribution": Constants.offer_choices[10]}
        )
        self.submit(views.Results)

    def validate_play(self):
        pass
