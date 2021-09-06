import { useState, useEffect } from 'react';

import { gameService } from '../api/game.service';

import { Game as GameComponent } from '../components';
import { useMoving } from '../hooks/useMoving';
import { Game as GameModel } from '../models/game.model';
import { Map } from '../models/map.model';

export const Game = () => {
  const [game, setGame] = useState<GameModel | null>(null);
  const [isGameOver, setIsGameOver] = useState(false);

  const startGame = async () => {
    const game = await gameService.startGame();
    setGame(game);
  }

  const stopGame = async () => {
    await gameService.stopGame();
    setGame(null);
    setIsGameOver(true);
  }

  useMoving(!!game, game?.map as Map, (position) => setGame({ ...game!, playerPosition: position }));

  useEffect(() => {
    if (game) {
      gameService.sendMakeMove(game!.playerPosition.x, game!.playerPosition.y);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [game?.playerPosition]);

  useEffect(() => {
    if (game && !gameService.isRegisteredOnEnemyPositionsHandler() && !gameService.isRegisteredOnGameOverHandler()) {
      gameService.registerOnEnemyPositionsHandler((enemyPositions) => {
        setGame({ ...game, enemyPositions });
      });

      gameService.registerOnGameOverHandler(() => {
        stopGame()
      });

      return () => {
        gameService.removeOnEnemyPositionsHandler();
        gameService.removeOnGameOverHandler();
      }
    }
  }, [game]);

  return (
    <div>
      <button onClick={startGame} color="greed">Start Game</button>
      {isGameOver && <p>GAME OVER</p>}
      <GameComponent game={game} />
    </div>
  )
}
