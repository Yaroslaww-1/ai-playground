import React, { useState, useEffect } from 'react';
import { EnemyTile, PlayerTile } from '..';

import { Game as GameModel } from '../../models/game.model';
import { MapTile } from '../../models/map-tile.enum';
import { Map } from '../../models/map.model';

import { EmptyTile } from '../tiles/empty-tile/empty-tile.component';
import { WallTile } from '../tiles/wall-tile/wall-tile.component';

import './index.css';

export const Game = ({ game } : { game: GameModel | null }) => {
  const [map, setMap] = useState<Map | null>(null);

  useEffect(() => {
    if (game) {
      setMap(game.map);
    }
  }, [game])

  const getTileComponent = (tile: MapTile, x: number, y: number) => {
    const commonProps = { key: `${x}-${y}` };

    if (isPlayerTile(x, y)) {
      return <PlayerTile {...commonProps} />
    }

    if (isEnemyTile(x, y)) {
      return <EnemyTile {...commonProps} />
    }

    switch (tile) {
      case MapTile.Empty: return <EmptyTile {...commonProps} />
      case MapTile.Wall: return <WallTile {...commonProps} />
    }
  }

  const isPlayerTile = (x: number, y: number) => {
    return x === game?.playerPosition.x && y === game.playerPosition.y;
  }

  const isEnemyTile = (x: number, y: number) => {
    return game?.enemyPositions.some(p => p.x === x && p.y === y);
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
