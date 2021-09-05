import { MapTile } from "./map-tile.enum";

export interface Map {
  tiles: MapTile[][];
  width: number;
  height: number;
}
