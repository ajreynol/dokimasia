; AndOrXorConcatPullUp (xor): constant last in concat (pullup rule 1)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 2))
(declare-const y (_ BitVec 8))
(assert (not (= (bvxor x (concat a b #x0)) (concat (bvxor ((_ extract 7 4) x) (concat a b)) (bvxor ((_ extract 3 0) x) #x0)))))
(check-sat)
