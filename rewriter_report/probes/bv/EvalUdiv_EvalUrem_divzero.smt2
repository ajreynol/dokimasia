; EvalUdiv/EvalUrem: SMT-LIB total semantics (x/0 = ones, x%0 = x) incl. width 1, non-pow2 divisors.
; EXPECT: unsat
(set-logic QF_BV)
(assert (not (and
  (= (bvudiv #b0101 #b0000) #b1111) (= (bvudiv #b0 #b0) #b1) (= (bvudiv #b1 #b0) #b1)
  (= (bvudiv #b110 #b011) #b010) (= (bvudiv #b111 #b111) #b001) (= (bvudiv #b010 #b101) #b000)
  (= (bvurem #b0101 #b0000) #b0101) (= (bvurem #b0 #b0) #b0) (= (bvurem #b1 #b0) #b1)
  (= (bvurem #b111 #b011) #b001) (= (bvurem #b010 #b101) #b010) (= (bvurem #b101 #b101) #b000))))
(check-sat)
