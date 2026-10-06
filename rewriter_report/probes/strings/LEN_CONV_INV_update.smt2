; len(update(x,n,y)) = len x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.len (str.update x n y)) (str.len x))))
(check-sat)
