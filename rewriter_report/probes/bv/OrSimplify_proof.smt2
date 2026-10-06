; OrSimplify: constant merge + duplicate removal (MACRO_BV_OR_SIMPLIFY)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvor x #b0100 y x #b0001) (bvor #b0101 x y))))
(check-sat)
