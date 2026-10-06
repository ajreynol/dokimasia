; Proof probe: (bvurem x 2^k) -> concat(0, x[k-1:0]) incl. k=n-1 (msb constant) and k=0 (urem 1).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (or (not (= (bvurem x #b0100) (concat #b00 ((_ extract 1 0) x))))
            (not (= (bvurem x #b1000) (concat #b0 ((_ extract 2 0) x))))
            (not (= (bvurem x #b0001) #b0000))))
(check-sat)
