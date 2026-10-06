; substr(x, len(substr(x,n,m)) + len(x) - ... ) approx: start len x - len(substr x n m) + len(x) >= len(x)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr x (- (* 2 (str.len x)) (str.len (str.substr x n m))) n) "")))
(check-sat)
