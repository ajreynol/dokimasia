; substr start len(x)+indexof(y,z,0)+1 >= len x via indexof>=-1 approx -> empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (+ (str.len x) (str.indexof y z 0) 1) n) "")))
(check-sat)
