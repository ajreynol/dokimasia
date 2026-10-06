; EvalUlt/EvalUle/EvalSlt/EvalSle/EvalComp/EvalNeg/EvalNot/EvalSignExtend on signed/unsigned edge constants.
; EXPECT: unsat
(set-logic QF_BV)
(assert (not (and
  (bvult #b0111 #b1000) (not (bvult #b1000 #b0111)) (not (bvult #b1 #b1)) (bvule #b1 #b1)
  (bvslt #b1000 #b0111) (not (bvslt #b0111 #b1000)) (bvslt #b1 #b0) (not (bvslt #b0 #b1))
  (bvsle #b1000 #b1000) (not (bvsle #b0000 #b1111)) (bvsle #b1 #b0)
  (= (bvcomp #b101 #b101) #b1) (= (bvcomp #b101 #b100) #b0)
  (= (bvneg #b1000) #b1000) (= (bvneg #b1) #b1) (= (bvneg #b0001) #b1111)
  (= (bvnot #b1010) #b0101) (= (bvnot #b0) #b1)
  (= ((_ sign_extend 3) #b1) #b1111) (= ((_ sign_extend 2) #b01) #b0001) (= ((_ sign_extend 0) #b10) #b10)
  (= (bvmul #b111 #b111) #b001) (= (bvadd #b111 #b001) #b000))))
(check-sat)
