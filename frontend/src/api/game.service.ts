import { Game } from "../models/game.model";
import { API_URL } from "./constants";

export class GameService {
  static async getGame(): Promise<Game> {
    const response = await fetch(`${API_URL}/game`);
    const data = await response.json();
    return data as Game;
  }

  static async startGame(): Promise<Game> {
    const response = await fetch(`${API_URL}/game/start`, { method: 'POST' });
    const data = await response.json();
    return data as Game;
  }
}