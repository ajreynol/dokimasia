; Differential edge: 1-bit x (msb position 0), sext by 3, constants at 1, 2, ~0, 0 on both sides.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(define-fun S () (_ BitVec 4) ((_ sign_extend 3) x))
(assert (or (not (= (bvult S #x1) (= x #b0))) (not (= (bvult S #x2) (= x #b0)))
            (bvult S #x0) (not (= (bvult S #xf) (= x #b0)))
            (not (= (bvult #x0 S) (= x #b1))) (not (= (bvult #x1 S) (= x #b1)))
            (not (= (bvult #xe S) (= x #b1))) (bvult #xf S)))
(check-sat)
