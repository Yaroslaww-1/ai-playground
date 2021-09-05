import { Map } from "../models/map.model";
import { API_URL } from "./constants";

export class MapService {
  static url = `${API_URL}/map`

  static async getMap(): Promise<Map> {
    const response = await fetch(this.url);
    const data = await response.json();
    return data.map as Map;
  }
}