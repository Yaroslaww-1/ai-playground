import React, { useState, useEffect } from 'react';

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
    switch (tile) {
      case MapTile.Empty: return <EmptyTile {...commonProps} />
      case MapTile.Wall: return <WallTile {...commonProps} />
    }
  }

  return (
    <div className="game" style={{ maxWidth: `calc(${map?.length} * 70px)` }}>
      {
        map && map.map((row, y) =>
          row.map((tile, x) => getTileComponent(tile, x, y))
        )
      }
    </div>
  )
}
