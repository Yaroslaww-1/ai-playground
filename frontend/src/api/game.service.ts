import { Enemy } from "../models/enemy.model";
import { Game } from "../models/game.model";
import { Score } from "../models/score.model";
import { API_URL, WS_API_URL } from "./constants";

class GameService {
  private ws!: WebSocket;
  private handlers: Map<string, (payload: any) => void> = new Map();

  constructor() {
    this.registerOnMessage = this.registerOnMessage.bind(this);
  }

  async getGame(): Promise<Game> {
    const response = await fetch(`${API_URL}/game`);
    const data = await response.json();
    return data as Game;
  }

  async startGame(): Promise<Game> {
    const response = await fetch(`${API_URL}/game/start`, { method: 'POST' });
    const data = await response.json();

    await this.initSocket();

    return data as Game;
  }

  async stopGame(): Promise<void> {
    this.sendStopGame();
  }

  private async initSocket() {
    const connectionString = `${WS_API_URL}/game/`;
    this.ws = new WebSocket(connectionString);
    this.ws.onmessage = this.registerOnMessage;
    await new Promise<void>((resolve) => {
      this.ws.onopen = () => {
        this.sendStartGame();
      return resolve();
    }});
  }

  // Inbound
  private registerOnMessage(ev: MessageEvent<any>) {
    const message = JSON.parse(ev.data);
    this.handlers.forEach((handler, handlerType) => {
      if (message.type === handlerType) {
        handler(message.payload);
      }
    })
  }

  registerOnEnemyPositionsHandler(callback: (enemies: Enemy[]) => void) {
    this.handlers.set('NEW_ENEMY_POSITIONS', callback);
    console.log(this.handlers.get('NEW_ENEMY_POSITIONS'))
  }

  isRegisteredOnEnemyPositionsHandler() {
    return this.handlers.has('NEW_ENEMY_POSITIONS');
  }

  removeOnEnemyPositionsHandler() {
    this.handlers.delete('NEW_ENEMY_POSITIONS');
  }

  registerOnGameOverHandler(callback: () => void) {
    this.handlers.set('GAME_OVER', callback);
  }

  isRegisteredOnGameOverHandler() {
    return this.handlers.has('GAME_OVER');
  }

  removeOnGameOverHandler() {
    this.handlers.delete('GAME_OVER');
  }

  registerOnNewScoreHandler(callback: (score: Score) => void) {
    this.handlers.set('NEW_SCORE', callback);
  }

  isRegisteredOnNewScoreHandler() {
    return this.handlers.has('NEW_SCORE');
  }

  removeOnNewScoreHandler() {
    this.handlers.delete('NEW_SCORE');
  }

  // Outbound
  private sendMessage(payload: any) {
    if (this.ws) {
      this.ws.send(JSON.stringify(payload));
    }
  }

  sendMakeMove(x: number, y: number) {
    const payload = {
      event: "MOVE",
      payload: { x, y, }
    };

    this.sendMessage(payload);
  }

  private sendStartGame() {
    const payload = {
      event: "START",
    };

    this.sendMessage(payload);
  }

  private sendStopGame() {
    const payload = {
      event: "STOP",
    };

    this.sendMessage(payload);
  }
}

export const gameService = new GameService();
