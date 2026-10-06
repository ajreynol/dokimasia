; Ground version of MultSltMult_nary_concat: fires at pre-rewrite (before constant folding); true value is sat (-31 <s 12).
; EXPECT: sat
(set-logic QF_BV)
(assert (bvslt (bvmul (concat #b00 (bvadd #b01 #b01) #b11) ((_ sign_extend 3) #b011)) (bvmul (concat #b00 #b01 #b00) ((_ sign_extend 3) #b011))))
(check-sat)
