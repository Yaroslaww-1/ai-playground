import { Map } from "./map.model";
import { Position } from "./position.model";

export interface Game {
  map: Map;
  playerPosition: Position;
  ghostsPositions: Position[];
}