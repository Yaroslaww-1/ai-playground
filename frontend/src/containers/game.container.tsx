import { useState, useEffect } from 'react';

import { gameService } from '../api/game.service';

import { Game as GameComponent } from '../components';
import { GameOver } from '../components/game-over/game-over';
import { Score } from '../components/score/score';
import { StartGame } from '../components/start-game/start-game';
import { useMoving } from '../hooks/useMoving';
import { Map as MapModel } from '../models/map.model';
import { Position } from '../models/position.model';
import { Score as ScoreModel } from '../models/score.model';

export const Game = () => {
  const [playerPosition, setPlayerPosition] = useState<Position | null>(null);
  const [enemyPositions, setEnemyPositions] = useState<Position[]>([]);
  const [map, setMap] = useState<MapModel | null>(null);
  const [score, setScore] = useState<ScoreModel | null>(null);
  const [isGameOver, setIsGameOver] = useState(false);
  const [isGameInProgress, setIsGameInProgress] = useState(false);

  const startGame = async () => {
    const game = await gameService.startGame();
    setIsGameInProgress(true);

    setPlayerPosition(game.playerPosition);
    setEnemyPositions(game.enemyPositions);
    setMap(game.map);
  }

  const stopGame = async () => {
    await gameService.stopGame();
    setIsGameOver(true);
    setIsGameInProgress(false);

    setPlayerPosition(null);
    setEnemyPositions([]);
    setMap(null);
  }

  console.log('render');

  useMoving(isGameInProgress, map!, setPlayerPosition);

  useEffect(() => {
    if (isGameInProgress) {
      gameService.sendMakeMove(playerPosition!.x, playerPosition!.y);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playerPosition]);

  useEffect(() => {
    const isHandlersNotRegistered = !gameService.isRegisteredOnEnemyPositionsHandler() &&
      !gameService.isRegisteredOnGameOverHandler() &&
      !gameService.isRegisteredOnNewScoreHandler();
      console.log(isHandlersNotRegistered);
    if (isGameInProgress && isHandlersNotRegistered) {
      gameService.registerOnEnemyPositionsHandler((enemyPositions) => {
        console.log('setGame');
        setEnemyPositions(enemyPositions);
      });

      gameService.registerOnGameOverHandler(() => {
        stopGame()
      });

      gameService.registerOnNewScoreHandler((score) => {
        setScore(score);
      })
    }

    // return () => {
    //   gameService.removeOnEnemyPositionsHandler();
    //   gameService.removeOnGameOverHandler();
    //   gameService.removeOnNewScoreHandler();
    // }
  }, [isGameInProgress]);

  // useEffect(() => {
    // gameService.removeOnEnemyPositionsHandler();
    // gameService.removeOnGameOverHandler();
    // gameService.removeOnNewScoreHandler();
  // }, [game])

  return (
    <div>
      {isGameInProgress 
        ? <Score score={score?.score ?? 0} />
        : <StartGame onClick={startGame} />
      }
      {isGameOver 
        ? <GameOver />
        : <GameComponent playerPosition={playerPosition!} enemyPositions={enemyPositions!} map={map!} score={score} />
      }
    </div>
  )
}
