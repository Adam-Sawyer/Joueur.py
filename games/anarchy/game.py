# Generated by Creer at 12:13AM on November 01, 2015 UTC, git hash: '1b69e788060071d644dd7b8745dca107577844e1'
# This is a simple class to represent the Game object in the game. You can extend it by adding utility functions here in this file.

from joueur.base_game import BaseGame

# import game objects
from games.anarchy.building import Building
from games.anarchy.fire_department import FireDepartment
from games.anarchy.forecast import Forecast
from games.anarchy.game_object import GameObject
from games.anarchy.player import Player
from games.anarchy.police_department import PoliceDepartment
from games.anarchy.warehouse import Warehouse
from games.anarchy.weather_station import WeatherStation

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add addtional import(s) here
# <<-- /Creer-Merge: imports -->>

class Game(BaseGame):
    """ The class representing the Game in the Anarchy game.

    Two player grid based game where each player tries to burn down the other player's buildings. Let it burn!
    """

    def __init__(self):
        """ initializes a Game with basic logic as provided by the Creer code generator
        """
        BaseGame.__init__(self)

        # private attributes to hold the properties so they appear read only
        self._base_bribes_per_turn = 0
        self._buildings = []
        self._current_forecast = None
        self._current_player = None
        self._current_turn = 0
        self._forecasts = []
        self._game_objects = {}
        self._map_height = 0
        self._map_width = 0
        self._max_fire = 0
        self._max_forecast_intensity = 0
        self._max_turns = 100
        self._next_forecast = None
        self._players = []
        self._session = ""

        self.name = "Anarchy"

        self._game_object_classes = {
            'PoliceDepartment': PoliceDepartment,
            'FireDepartment': FireDepartment,
            'Building': Building,
            'GameObject': GameObject,
            'Player': Player,
            'Forecast': Forecast,
            'Warehouse': Warehouse,
            'WeatherStation': WeatherStation
        }


    @property
    def base_bribes_per_turn(self):
        """How many bribes players get at the beginning of their turn, not counting their burned down Buildings.
        """
        return self._base_bribes_per_turn


    @property
    def buildings(self):
        """All the buildings in the game.
        """
        return self._buildings


    @property
    def current_forecast(self):
        """The current Forecast, which will be applied at the end of the turn.
        """
        return self._current_forecast


    @property
    def current_player(self):
        """The player whose turn it is currently. That player can send commands. Other players cannot.
        """
        return self._current_player


    @property
    def current_turn(self):
        """The current turn number, starting at 0 for the first player's turn
        """
        return self._current_turn


    @property
    def forecasts(self):
        """All the forecasts in the game, indexed by turn number.
        """
        return self._forecasts


    @property
    def game_objects(self):
        """A mapping of every game object's ID to the actual game object. Primarily used by the server and client to easily refer to the game objects via ID.
        """
        return self._game_objects


    @property
    def map_height(self):
        """The width of the entire map along the vertical (y) axis.
        """
        return self._map_height


    @property
    def map_width(self):
        """The width of the entire map along the horizontal (x) axis.
        """
        return self._map_width


    @property
    def max_fire(self):
        """The maximum amount of fire value for any Building.
        """
        return self._max_fire


    @property
    def max_forecast_intensity(self):
        """The maximum amount of intensity value for any Forecast.
        """
        return self._max_forecast_intensity


    @property
    def max_turns(self):
        """The maximum number of turns before the game will automatically end.
        """
        return self._max_turns


    @property
    def next_forecast(self):
        """The next Forecast, which will be applied at the end of your opponent's turn. This is also the Forecast WeatherStations can control this turn.
        """
        return self._next_forecast


    @property
    def players(self):
        """List of all the players in the game.
        """
        return self._players


    @property
    def session(self):
        """A unique identifier for the game instance that is being played.
        """
        return self._session



    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you want to add any client side logic (such as state checking functions) this is where you can add them
    # <<-- /Creer-Merge: functions -->>
