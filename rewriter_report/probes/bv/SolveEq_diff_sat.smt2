; SolveEq differential: coefficient compare (unsigned >) with wrap; 3x+y = x+y+2 is sat (x=1)
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (= (bvadd (bvmul x #b0011) y) (bvadd x y #b0010)))
(check-sat)
