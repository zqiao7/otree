# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_is_missing_players', otree.db.models.BooleanField(default=False, db_index=True, choices=[(True, 'Yes'), (False, 'No')])),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('provision_success', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('num_of_members', otree.db.models.IntegerField(null=True)),
                ('session', otree.db.models.ForeignKey(related_name='serial_cost_sharing_group', to='otree.Session')),
            ],
            options={
                'db_table': 'serial_cost_sharing_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_index_in_game_pages', otree.db.models.PositiveIntegerField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('payoff', otree.db.models.CurrencyField(null=True, max_digits=12)),
                ('private_value', otree.db.models.CurrencyField(null=True, max_digits=12)),
                ('contribution', otree.db.models.CharField(max_length=500, null=True, choices=[(b'0', b'0'), (b'1/3', b'1/3'), (b'1/2', b'1/2')])),
                ('member', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('share', otree.db.models.CharField(max_length=500, null=True, choices=[(b'0', b'0'), (b'1/3', b'1/3'), (b'1/2', b'1/2')])),
                ('group', otree.db.models.ForeignKey(to='serial_cost_sharing.Group', null=True)),
                ('participant', otree.db.models.ForeignKey(related_name='serial_cost_sharing_player', to='otree.Participant')),
                ('session', otree.db.models.ForeignKey(related_name='serial_cost_sharing_player', to='otree.Session')),
            ],
            options={
                'db_table': 'serial_cost_sharing_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', otree.db.models.PositiveIntegerField(null=True, db_index=True)),
                ('session', otree.db.models.ForeignKey(related_name='serial_cost_sharing_subsession', to='otree.Session', null=True)),
            ],
            options={
                'db_table': 'serial_cost_sharing_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=otree.db.models.ForeignKey(to='serial_cost_sharing.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=otree.db.models.ForeignKey(to='serial_cost_sharing.Subsession'),
        ),
    ]
