"""
PYVED game engine by moonb3ndr [thomas.iw@kata.games] et al.

Visit https://kata.games to learn more!
"""


import pyved_engine as _engine
# _engine.bootstrap_e()

from pyved_engine import component, entity, EntityManager, System, SystemManager
from pyved_engine.core.events import EvManager, EvListener
from pyved_engine import game_events_enum, get_ev_manager, init, quit, get_surface, flip


def pygame_proxy():
    _engine.bootstrap_e()
    return _engine.pygame


# lists what should be interpreted by import *
# this overrides the default of hiding everything that begins with an underscore
__all__ = [
    component, entity, EntityManager, System, SystemManager,
    EvManager, EvListener,
    game_events_enum, get_ev_manager, init, quit, get_surface, flip,
    pygame_proxy
]
