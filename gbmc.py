from dataclasses import dataclass
from random import random

@dataclass
class Player:
    id: int
    is_dead: bool = False
    num_attempt_at_death: int = -1 # how many attempts have been made at time of death (-1 if not dead)
    panel_at_death: int = -1 # which panel caused the player's death (-1 if not dead)

class GlassBridge:

    def __init__(self, bridge_size=18, num_player=16, prob_success=0.5, log_enabled=True):

        # invariable
        self.bridge_size = bridge_size
        self.num_player_total = num_player
        self.prob_success = prob_success
        self.log_enabled = log_enabled

        # variable
        self.num_player_alive = num_player
        self.has_ended = False
        self.num_attempt = 0 # number of attempts made (only including by the player at the front)
        self.curr_panel_id = 1 # which panel the player at the front will attempt next
        self.curr_player_id = 1 # the player who will attempt next
        self.players = { i: Player(id=i) for i in range(1, num_player + 1) }

    def step(self):        
        if self.has_ended:
            raise ValueError("game has already ended")

        self.num_attempt += 1
        self.log_info(f"[attempt {self.num_attempt}] player {self.curr_player_id} attempts panel {self.curr_panel_id}")
        
        if random() < self.prob_success: # success
            self.log_info("[success]")
        else: # fail
            # update death info for current player
            self.log_info("[failure]")
            curr_player = self.get_current_player()
            curr_player.is_dead = True
            curr_player.num_attempt_at_death = self.num_attempt
            curr_player.panel_at_death = self.curr_panel_id
            self.num_player_alive -= 1

            # prep next player
            self.curr_player_id += 1

        self.curr_panel_id += 1
        if self.curr_panel_id == self.bridge_size + 1: # reached the end
            self.has_ended = True
            surviving_players_str = ", ".join([str(player.id) for player in self.get_surviving_players()])
            self.log_info(f"[game over] {self.num_player_alive} players survived ({surviving_players_str})")
        
        if self.num_player_alive == 0:
            self.has_ended = True
            self.log_info("[game over] no players survived")

    def run(self):
        while not self.has_ended:
            self.step()

    def get_current_player(self) -> Player:
        return self.players[self.curr_player_id]
    
    def get_surviving_players(self) -> list[Player]:
        return [player for player in self.players.values() if not player.is_dead]

    def log_info(self, info):
        if self.log_enabled:
            print(info)