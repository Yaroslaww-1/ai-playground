import { useState, useEffect } from 'react';

import { gameService } from '../api/game.service';

import { Game as GameComponent } from '../components';
import { useKeyPress } from '../hooks';
import { Game as GameModel } from '../models/game.model';
import { MapTile } from '../models/map-tile.enum';
import { Position } from '../models/position.model';

export const Game = () => {
  const [game, setGame] = useState<GameModel | null>(null);

  const startGame = async () => {
    const game = await gameService.startGame();
    setGame(game);
  }

  const stopGame = async () => {
    await gameService.stopGame();
    setGame(null);
  }

  const isPositionAvailableForMove = (position: Position) => {
    const { x, y } = position;
    return game?.map.tiles[y][x] !== MapTile.Wall;
  }

  const moveUp = () => {
    const { x, y } = game!.playerPosition;
    const newPosition = { x, y: y - 1 };
    if (game && y > 0 && isPositionAvailableForMove(newPosition)) {
      setGame({ ...game, playerPosition: newPosition });
    }
  }

  const moveDown = () => {
    const { x, y } = game!.playerPosition;
    const newPosition = { x, y: y + 1 };
    if (game && y < game!.map.height - 1 && isPositionAvailableForMove(newPosition)) {
      setGame({ ...game, playerPosition: newPosition });
    }
  }

  const moveRight = () => {
    const { x, y } = game!.playerPosition;
    const newPosition = { x: x + 1, y };
    if (game && x < game!.map.width - 1 && isPositionAvailableForMove(newPosition)) {
      setGame({ ...game, playerPosition: newPosition });
    }
  }

  const moveLeft = () => {
    const { x, y } = game!.playerPosition;
    const newPosition = { x: x - 1, y };
    if (game && x > 0 && isPositionAvailableForMove(newPosition)) {
      setGame({ ...game, playerPosition: newPosition });
    }
  }

  useKeyPress('ArrowUp', moveUp);
  useKeyPress('ArrowDown', moveDown);
  useKeyPress('ArrowRight', moveRight);
  useKeyPress('ArrowLeft', moveLeft);

  useEffect(() => {
    if (game) {
      console.log('sendMakeMove');
      gameService.sendMakeMove(game!.playerPosition.x, game!.playerPosition.y);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [game?.playerPosition]);

  useEffect(() => {
    if (game && !gameService.isRegisteredOnEnemyPositionsHandler()) {
      gameService.registerOnEnemyPositionsHandler((enemyPositions) => {
        console.log('registerOnEnemyPositionsHandler triggered', game);
          setGame({ ...game, enemyPositions });
      });

      return () => {
        gameService.removeOnEnemyPositionsHandler();
      }
    }
  }, [game]);

  return (
    <div>
      <button onClick={startGame} color="greed">Start Game</button>
      <button onClick={stopGame} color="red">Stop Game</button>
      <GameComponent game={game} />
    </div>
  )
}
