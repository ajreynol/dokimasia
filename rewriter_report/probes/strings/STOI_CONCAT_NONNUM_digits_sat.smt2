; concat whose constant components are all digits must not be folded
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)(declare-const y String)
(assert (= (str.to_int (str.++ x "12" y)) 5120))
(check-sat)
