import json
import threading

from channels.generic.websocket import JsonWebsocketConsumer

from pacman.app_state import AppState
from pacman.serializers import PositionSerializer, ScoreSerializer


class PacmanConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = 0 #game is single-player, so only one room is available
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print('Disconnected')
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        AppState.game.stop()

    def receive(self, text_data):
        response = json.loads(text_data)
        event = response.get('event', None)
        payload = response.get('payload', None)
        if event == 'START':
            AppState.game.start(
                self.send_new_enemy_positions_message,
                self.send_game_over_message,
                self.score_changed_listener)
        if event == 'STOP':
            AppState.game.stop()
        if event == 'MOVE':
            if payload is not None:
                AppState.game.set_player_position(payload['x'], payload['y'])

    def send_message(self, type, payload):
        self.send(text_data=json.dumps({
            'type': type,
            'payload': payload,
        }))

    def send_new_enemy_positions_message(self, new_enemy_positions):
        self.send_message('NEW_ENEMY_POSITIONS', list(map(PositionSerializer.to_json, new_enemy_positions)))

    def send_game_over_message(self):
        self.send_message('GAME_OVER', {})

    def score_changed_listener(self, new_score):
        self.send_message('NEW_SCORE', ScoreSerializer.to_json(new_score))
