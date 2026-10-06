; AndOrXorConcatPullUp (or): const in middle with 2-child prefix and suffix, n-ary x
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const y (_ BitVec 8))
(declare-const a (_ BitVec 1))
(declare-const b (_ BitVec 1))
(declare-const c (_ BitVec 2))
(declare-const d (_ BitVec 2))
(assert (not (= (bvor x y (concat a b #b00 c d)) (concat (bvor ((_ extract 7 6) (bvor x y)) (concat a b)) (bvor ((_ extract 5 4) (bvor x y)) #b00) (bvor ((_ extract 3 0) (bvor x y)) (concat c d))))))
(check-sat)
