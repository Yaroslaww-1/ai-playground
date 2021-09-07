import { useState } from "react";

import { useKeyPress, useInterval } from ".";
import { GAME_LOOP_INTERVAL } from "../constants/game-settings.constants";
import { Direction } from "../enums/direction.enum";
import { animateMoving } from "../helpers/animation.helper";
import { MapTile } from "../models/map-tile.enum";
import { Map } from "../models/map.model";
import { Position } from "../models/position.model";

export const useMoving = (isGameInProgress: boolean, map: Map, updatePosition: (newPosition: Position) => void) => {
  const [isMoving, setIsMoving] = useState<boolean>(false);
  const [position, setPosition] = useState<Position>({ x: 0, y: 0 });
  const [movingDirection, setMovingDirection] = useState<Direction>(Direction.UP);

  const isPositionAvailableForMove = (x: number, y: number) => {
    if (!isGameInProgress) return false;
    if (x < 0 || x >= map.width) return false;
    if (y < 0 || y >= map.height) return false;
    return map.tiles[y][x] !== MapTile.Wall;
  }

  const move = (direction: Direction, currentX: number, currentY: number) => {
    let newX = currentX;
    let newY = currentY;
    switch (direction) {
      case Direction.UP: {
        newY--;
        break;
      }
      case Direction.DOWN: {
        newY++;
        break;
      }
      case Direction.RIGHT: {
        newX++;
        break;
      }
      case Direction.LEFT: {
        newX--;
        break;
      }
    }
    if (isPositionAvailableForMove(newX, newY)) {
      return { x: newX, y: newY };
    } else {
      return { x: currentX, y: currentY };
    }
  }

  const startMoving = (direction: Direction) => () => {
    if (!isGameInProgress) return;
    setMovingDirection(direction);
    setIsMoving(true);
  }

  useKeyPress('ArrowUp', startMoving(Direction.UP));
  useKeyPress('ArrowDown', startMoving(Direction.DOWN));
  useKeyPress('ArrowRight', startMoving(Direction.RIGHT));
  useKeyPress('ArrowLeft', startMoving(Direction.LEFT));

  useInterval(() => {
    if (!isMoving) return;

    const newPosition = move(movingDirection, position.x, position.y);

    if (newPosition.x !== position.x || newPosition.y !== position.y) {
      animateMoving(movingDirection).then(() => {
        setPosition(newPosition);
        updatePosition(newPosition);
      });
    } else {
      setIsMoving(false);
    }
  }, isGameInProgress ? GAME_LOOP_INTERVAL : null);
};
