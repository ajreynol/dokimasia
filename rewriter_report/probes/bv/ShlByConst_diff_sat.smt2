; ShlByConst: differential, (bvshl x 7) = #x80 sat at width 8
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(assert (= (bvshl x #x07) #x80))
(check-sat)
