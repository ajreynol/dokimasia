; len(substr(x,n,m)) <= len(x)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (> (str.len (str.substr x n m)) (str.len x)))
(check-sat)
