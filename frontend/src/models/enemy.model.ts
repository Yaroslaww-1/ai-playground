import { Direction } from "../enums/direction.enum";

export interface Enemy {
  x: number;
  y: number;
  direction: Direction;
  id: number;
}
