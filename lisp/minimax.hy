(defclass Position []
  (defn __init__ [self x y]
    (setv self.x x)
    (setv self.y y)
  )
)

(defclass Map []
  (defn __init__ [self tiles width height]
    (setv self.tiles tiles)
    (setv self.width width)
    (setv self.height height)
  )

  (defn is_open_position [self position]
    (if (do (< position.x self.width) (>= position.x 0) (< position.y self.height) (>= position.y 0))
      (do
        (setv value (get (get self.tiles position.y) position.x))
        (= value 0)
      )
      (do
        False
      )
    )
  )
)

(setv tiles [])
(.append tiles [1 1 0 1 1])
(.append tiles [1 0 0 0 1])
(.append tiles [1 0 0 0 1])
(.append tiles [1 0 0 0 1])
(.append tiles [1 1 1 1 1])
(setv map (Map tiles 5 5))

; --------------------------------------------------

(defclass Evaluator []
  (defn __init__ [self]
  )

  (defn evaluate [self current_position target_position]
    (setv def_x (* (- current_position.x target_position.x) (- current_position.x target_position.x)))
    (setv def_y (* (- current_position.y target_position.y) (- current_position.y target_position.y)))
    (** (+ def_x def_y) (/ 1 2))
  )
)

(setv evaluator (Evaluator))

(defclass MinimaxState []
  (defn __init__ [self cost depth player_position enemy_position]
    (setv self.cost cost)
    (setv self.depth depth)
    (setv self.player_position player_position)
    (setv self.enemy_position enemy_position)
  )

  (defn get_all_adjacent_positions [self position]
    (setv positions [])

    (setv next_possible_position (Position (+ position.x 1) position.y))
    (if (map.is_open_position next_possible_position)
      (.append positions next_possible_position)
    )

    (setv next_possible_position (Position (- position.x 1) position.y))
    (if (map.is_open_position next_possible_position)
      (.append positions next_possible_position)
    )

    (setv next_possible_position (Position position.x (+ position.y 1)))
    (if (map.is_open_position next_possible_position)
      (.append positions next_possible_position)
    )

    (setv next_possible_position (Position position.x (- position.y 1)))
    (if (map.is_open_position next_possible_position)
      (.append positions next_possible_position)
    )

    positions
  )
)

(defclass Minimax []
  (defn __init__ [self]
    (setv self.MAX_DEPTH 2)
  )

  (defn find_optimal_next_position [self state]
    (if (< state.depth self.MAX_DEPTH)
      (if (= (% state.depth 2) 0)
        (self.maximize state)
        (self.minimize state)
      )
      state
    )
  )

  (defn maximize [self state]
    (setv adjacent_positions (state.get_all_adjacent_positions state.player_position))
    (setv values
      (lfor adjacent_position adjacent_positions
        (self.find_optimal_next_position (
          MinimaxState
            (evaluator.evaluate adjacent_position state.enemy_position)
            (+ state.depth 1)
            adjacent_position
            state.enemy_position
          )
        )
      )
    )
    (setv max_value (MinimaxState -100000 0 (Position 0 0) (Position 0 0)))
    (for [value values]
      (if (< max_value.cost value.cost)
        (setv max_value value)
      )
    )
    (print "max_value: " max_value.player_position.x max_value.player_position.y)
    max_value
  )

  (defn minimize [self state]
    (setv adjacent_positions (state.get_all_adjacent_positions state.player_position))
    (setv values
      (lfor adjacent_position adjacent_positions
        (self.find_optimal_next_position (
          MinimaxState
            (evaluator.evaluate adjacent_position state.player_position)
            (+ state.depth 1)
            state.player_position
            adjacent_position
          )
        )
      )
    )
    (setv min_value (MinimaxState 100000 0 (Position 0 0) (Position 0 0)))
    (for [value values]
      (if (> min_value.cost value.cost)
        (setv min_value value)
      )
    )
    (print "min_value: " min_value.enemy_position.x min_value.enemy_position.y)
    min_value
  )
)

(setv initial_state (MinimaxState 0 0 (Position 2 0) (Position 2 3)))
(setv minimax (Minimax))
(setv next_state (minimax.find_optimal_next_position initial_state))
(print "Next position: " next_state.player_position.x next_state.player_position.y)