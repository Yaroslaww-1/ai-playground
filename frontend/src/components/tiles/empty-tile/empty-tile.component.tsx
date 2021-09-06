import React from 'react';

import { Tile } from '../../';

import './index.css';

export const EmptyTile = ({ withPoint = true }) => {
  return (
    <Tile className="empty-tile">
      {withPoint && <div className="point"></div>}
    </Tile>
  )
}
