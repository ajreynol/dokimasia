; Pull-up with two concat children that both have a middle constant: C++ pulls up the first, elaborator groups both.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 2))
(declare-const b (_ BitVec 2))
(declare-const c (_ BitVec 2))
(declare-const d (_ BitVec 2))
(assert (not (= (bvor (concat a #b00 b) (concat c #b11 d))
                (bvor (concat a #b00 b) (concat c #b11 d) #b000000))))
(assert (not (= (bvor (concat a #b00 b) (concat c #b11 d))
                (concat (bvor a c) #b11 (bvor b d)))))
(check-sat)
