; substr start len(x)+to_int(y)+1 >= len x via to_int>=-1 -> empty
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (+ (str.len x) (str.to_int y) 1) n) "")))
(check-sat)
