; Proof probe (default options): (= zext(1,x) c) with c[n-1]=1, the case where RARE bv-zero-extend-eq-const's chi=extract(nm-1,n-1) has m+1 bits vs (@bv 0 m).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 2))
(assert (or (not (= (= ((_ zero_extend 1) x) #b01) (= x #b1)))
            (not (= (= ((_ zero_extend 2) y) #b0011) (= y #b11)))))
(check-sat)
