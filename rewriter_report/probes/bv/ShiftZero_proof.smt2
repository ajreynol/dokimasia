; Proof probe: shl/lshr/ashr of 0 by a variable amount -> 0 (ShiftZero / bv-{shl,lshr,ashr}-zero).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const a (_ BitVec 4))
(assert (or (not (= (bvshl #b0000 a) #b0000)) (not (= (bvlshr #b0000 a) #b0000))
            (not (= (bvashr #b0000 a) #b0000))))
(check-sat)
