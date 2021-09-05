import React, { useState, useEffect } from 'react';
import { MapService } from '../api/map.service';

import { Game as GameComponent } from '../components';
import { Game as GameModel } from '../models/game.model';

export const Game = () => {
  const [game, setGame] = useState<GameModel | null>(null);

  useEffect(() => {
    async function fetchGame() {
      const map = await MapService.getMap();
      setGame({
        map,
        playerPosition: { x: 0, y: 0 },
        ghostsPositions: [],
      });
    }

    fetchGame()
    
  }, []);

  return (
    <div>
      <button>Start Game</button>
      <GameComponent game={game} />
    </div>
  )
}
