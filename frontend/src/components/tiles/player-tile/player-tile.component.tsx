import React from 'react';

import { Tile } from '../..';

import './index.css';

import image from './player.png';

export const PlayerTile = () => {
  return (
    <Tile className="player-tile">
      <img src={image} height={50} width={50}></img>
    </Tile>
  )
}
