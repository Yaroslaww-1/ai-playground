import { useState, useEffect } from 'react';

import { gameService } from '../api/game.service';

import { Game as GameComponent } from '../components';
import { GameOver } from '../components/game-over/game-over';
import { Score } from '../components/score/score';
import { StartGame } from '../components/start-game/start-game';
import { useMoving } from '../hooks/useMoving';
import { Game as GameModel } from '../models/game.model';
import { Map } from '../models/map.model';
import { Score as ScoreModel } from '../models/score.model';

export const Game = () => {
  const [game, setGame] = useState<GameModel | null>(null);
  const [score, setScore] = useState<ScoreModel | null>(null);
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
    const isHandlersNotRegistered = !gameService.isRegisteredOnEnemyPositionsHandler() &&
      !gameService.isRegisteredOnGameOverHandler() &&
      !gameService.isRegisteredOnNewScoreHandler();
    if (game && isHandlersNotRegistered) {
      gameService.registerOnEnemyPositionsHandler((enemyPositions) => {
        setGame({ ...game, enemyPositions });
      });

      gameService.registerOnGameOverHandler(() => {
        stopGame()
      });

      gameService.registerOnNewScoreHandler((score) => {
        setScore(score);
      })

      return () => {
        gameService.removeOnEnemyPositionsHandler();
        gameService.removeOnGameOverHandler();
        gameService.removeOnNewScoreHandler();
      }
    }
  }, [game]);

  return (
    <div>
      {game 
        ? <Score score={score?.score ?? 0} />
        : <StartGame onClick={startGame} />
      }
      {isGameOver 
        ? <GameOver />
        : <GameComponent game={game} score={score} />
      }
    </div>
  )
}
