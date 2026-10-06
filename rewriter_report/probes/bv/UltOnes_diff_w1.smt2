; UltOne/UltOnes ordering at width 1: (bvult b #b1) sat with b=0
; EXPECT: sat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (bvult b #b1))
(check-sat)
