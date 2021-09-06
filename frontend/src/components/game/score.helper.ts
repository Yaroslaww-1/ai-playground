import { Position } from "../../models/position.model";
import { Score } from "../../models/score.model";

export class ScoreHelper {
  private positionsWithPointsMap: Map<string, boolean> = new Map();

  constructor(private readonly score: Score | null) {
    if (score) this.initializePositionsWithPointsMap();
  }

  isPositionWithPoint(position: Position) {
    return this.positionsWithPointsMap.has(this.getPositionKey(position));
  }

  private getPositionKey(position: Position) {
    return `${position.x}-${position.y}`;
  }

  private initializePositionsWithPointsMap = () => {
    const positionsMap = new Map<number, Map<number, boolean>>();
    for (const position of this.score!.availablePoints) {
      this.positionsWithPointsMap.set(this.getPositionKey(position), true);
    }
    return positionsMap;
  }
}