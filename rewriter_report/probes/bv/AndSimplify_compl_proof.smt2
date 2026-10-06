; AndSimplify: x & ~x with constants -> 0 (bv-and-simplify-1/2)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvand x #b0111 (bvnot x) y #b1101) #b0000)))
(check-sat)
