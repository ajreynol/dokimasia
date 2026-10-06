; ExtractNot: extract over bvnot pushed inside (bv-extract-not)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= ((_ extract 2 1) (bvnot x)) (bvnot ((_ extract 2 1) x)))))
(check-sat)
