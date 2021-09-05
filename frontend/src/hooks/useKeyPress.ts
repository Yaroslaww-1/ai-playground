import { useEffect } from "react";

export const useKeyPress = (targetKey: string, handler: () => void) => {
  function downHandler({ key }: KeyboardEvent) {
    if (key === targetKey) {
      handler();
    }
  }

  useEffect(() => {
    window.addEventListener("keydown", downHandler);

    return () => {
      window.removeEventListener("keydown", downHandler);
    };
  });
};
