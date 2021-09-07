import React, { useState, useEffect } from 'react';
import { EnemyTile, PlayerTile } from '..';
import { Enemy } from '../../models/enemy.model';

import { Game as GameModel } from '../../models/game.model';
import { MapTile } from '../../models/map-tile.enum';
import { Map as MapModel } from '../../models/map.model';
import { Position } from '../../models/position.model';
import { Score as ScoreModel } from '../../models/score.model';

import { EmptyTile } from '../tiles/empty-tile/empty-tile.component';
import { WallTile } from '../tiles/wall-tile/wall-tile.component';

import './index.css';
import { ScoreHelper } from './score.helper';

export const Game = (
  {
    enemies = [],
    map,
    playerPosition,
    score
  } :
  {
    enemies: Enemy[],
    map: MapModel,
    playerPosition: Position,
    score: ScoreModel | null,
  }
) => {
  const scoreHelper = new ScoreHelper(score);

  const getTileComponent = (tile: MapTile, x: number, y: number) => {
    const commonProps = { key: `${x}-${y}` };

    if (isPlayerTile(x, y)) {
      return <PlayerTile {...commonProps} />
    }

    if (isEnemyTile(x, y)) {
      return <EnemyTile enemy={getEnemyOnTile(x, y)} {...commonProps} />
    }

    switch (tile) {
      case MapTile.Empty: return <EmptyTile withPoint={isTileWithPoint(x, y)} {...commonProps} />
      case MapTile.Wall: return <WallTile {...commonProps} />
    }
  }

  const isPlayerTile = (x: number, y: number) => {
    return x === playerPosition.x && y === playerPosition.y;
  }

  const isEnemyTile = (x: number, y: number) => {
    return enemies.some(e => e.x === x && e.y === y);
  }

  const getEnemyOnTile = (x: number, y: number) => {
    return enemies.find(e => e.x === x && e.y === y)!;
  }

  const isTileWithPoint = (x: number, y: number) => {
    if (!score) return false;
    return scoreHelper.isPositionWithPoint({ x, y });
  }

  return (
    <div className="game" style={{ maxWidth: `calc(${map?.width} * 70px)` }}>
      {
        map && map.tiles.map((row, y) =>
          row.map((tile, x) => getTileComponent(tile, x, y))
        )
      }
    </div>
  )
}
