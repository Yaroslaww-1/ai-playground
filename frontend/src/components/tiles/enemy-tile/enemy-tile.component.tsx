import { Tile } from '../..';

import { Enemy } from '../../../models/enemy.model';
import { animateMoving } from '../../../helpers/animation.helper';

import './index.css';
import image from './enemy.png';

export const EnemyTile = ({ enemy } : { enemy: Enemy }) => {
  const enemyId = `${enemy.id}`;

  // TODO: enable
  // animateMoving(enemyId, enemy.direction);

  return (
    <Tile className="enemy-tile">
      <img src={image} height={50} width={50} alt="enemy" id={enemyId} />
    </Tile>
  )
}
