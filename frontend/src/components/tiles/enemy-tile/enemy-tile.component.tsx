import React from 'react';

import { Tile } from '../..';

import './index.css';

import image from './enemy.png';

export const EnemyTile = () => {
  return (
    <Tile className="enemy-tile">
      <img src={image} height={50} width={50}></img>
    </Tile>
  )
}
