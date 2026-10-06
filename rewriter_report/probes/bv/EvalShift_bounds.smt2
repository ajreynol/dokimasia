; EvalShl/EvalLshr/EvalAshr (in practice folded by *ByConst first): shift by 0, width-1, width, >width, all-ones.
; EXPECT: unsat
(set-logic QF_BV)
(assert (not (and
  (= (bvshl #b1011 #b0000) #b1011) (= (bvshl #b1011 #b0011) #b1000) (= (bvshl #b1011 #b0100) #b0000)
  (= (bvshl #b1011 #b0101) #b0000) (= (bvshl #b1011 #b1111) #b0000) (= (bvshl #b1 #b1) #b0)
  (= (bvlshr #b1011 #b0011) #b0001) (= (bvlshr #b1011 #b0100) #b0000) (= (bvlshr #b1011 #b1111) #b0000)
  (= (bvlshr #b1 #b1) #b0) (= (bvlshr #b1 #b0) #b1)
  (= (bvashr #b1011 #b0011) #b1111) (= (bvashr #b1011 #b0100) #b1111) (= (bvashr #b1011 #b0101) #b1111)
  (= (bvashr #b1011 #b1111) #b1111) (= (bvashr #b0111 #b0100) #b0000) (= (bvashr #b0111 #b1111) #b0000)
  (= (bvashr #b1011 #b0001) #b1101) (= (bvashr #b1 #b1) #b1) (= (bvashr #b0 #b1) #b0))))
(check-sat)
