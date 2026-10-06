; replace x (replace y x y) w
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace x (str.replace y x y) w) (str.replace x y w))))
(check-sat)
