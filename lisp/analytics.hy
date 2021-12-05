; https://www.rupython.com/x441-195-49670.html
(import [pandas [read_csv]])

(setv df (read_csv "./output.csv"))
(setv points (get df "points"))
(setv time (get df "time"))

(defn mean_value[column]
  (/ (column.sum) (len column))
)

(print "Time Expected Value:" (mean_value time))

(defn square[num]
  (* num num)
)

(defn substract[from, to]
  (- from to)
)

(defn dispersion2[column]
  (setv mean (mean_value column))
  (setv sum 0)
  (for [column_item (column.tolist)]
    (setv column_item_sum (/ (square column_item) (len column)))
    (setv sum (+ sum column_item_sum))
  )
  (- sum (square mean))
) 

(print "Points Dispersion Value:" (dispersion2 points))