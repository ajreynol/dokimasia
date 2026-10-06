; replace_all x x y with x nonempty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_all (str.++ "a" x) (str.++ "a" x) y) y)))
(check-sat)
