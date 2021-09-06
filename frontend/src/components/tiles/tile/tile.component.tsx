import React from 'react';

import './index.css';

export const Tile = ({ className = '', children } : React.PropsWithChildren<{ className: string }>) => {
  return (
    <div className={`tile ${className}`}>
      {children}
    </div>
  )
}
