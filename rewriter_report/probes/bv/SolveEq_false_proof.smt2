; SolveEq: (bvnot x) = x --> false; x+1 = x --> false (constant-only cases)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (or (= (bvnot (bvadd x y)) (bvadd x y)) (= (bvadd x y #b0001) (bvadd y x))))
(check-sat)
