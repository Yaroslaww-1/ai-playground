import { GAME_LOOP_INTERVAL } from "../constants/game-settings.constants";
import { Direction } from "../enums/direction.enum";

export const animateMoving = (elementId: string, direction: Direction) => {
  return new Promise<void>((resolve) => {
    let iteration = 0;
    const ANIMATION_INTERVAL = 10;
    const ITERATION_COUNT = GAME_LOOP_INTERVAL / ANIMATION_INTERVAL - 5; // 5 - empirical constant
    const STEP = 70 / (ITERATION_COUNT - 20); // 20 - empirical constant

    let interval = setInterval(() => {
      const playerElement = document.getElementById(elementId);

      if (iteration === ITERATION_COUNT || !playerElement) {
        clearInterval(interval);
        return resolve();
      }

      iteration++;

      switch (direction) {
        case Direction.UP: {
          playerElement.style.marginBottom = `${iteration * STEP}px`;
          break;
        }
        case Direction.DOWN: {
          playerElement.style.marginBottom = `${-iteration * STEP}px`;
          break;
        }
        case Direction.RIGHT: {
          playerElement.style.marginRight = `${-iteration * STEP}px`;
          break;
        }
        case Direction.LEFT: {
          playerElement.style.marginRight = `${iteration * STEP}px`;
          break;
        }
      }
    }, ANIMATION_INTERVAL);
  })
}
