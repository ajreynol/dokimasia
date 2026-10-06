; substr(str.at(x,n), 0, 1) = str.at(x,n)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr (str.at x n) 0 1) (str.at x n))))
(check-sat)
