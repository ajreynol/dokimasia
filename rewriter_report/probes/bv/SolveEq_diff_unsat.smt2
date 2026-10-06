; SolveEq differential: 2x = 2x+1 parity, unsat after cancellation
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (= (bvadd (bvmul x #b0010) y) (bvadd y (bvmul x #b0010) #b0001)))
(check-sat)
