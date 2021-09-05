import React from 'react';

import './index.css';

export const Tile = ({ className = '' } : { className: string }) => {
  return (
    <div className={`tile ${className}`}></div>
  )
}
