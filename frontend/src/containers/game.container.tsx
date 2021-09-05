import { useState, useEffect } from 'react';

import { GameService } from '../api/game.service';

import { Game as GameComponent } from '../components';
import { Game as GameModel } from '../models/game.model';

export const Game = () => {
  const [game, setGame] = useState<GameModel | null>(null);

  const startGame = async () => {
    const game = await GameService.startGame();
    setGame(game);
  }

  return (
    <div>
      <button onClick={startGame}>Start Game</button>
      <GameComponent game={game} />
    </div>
  )
}
