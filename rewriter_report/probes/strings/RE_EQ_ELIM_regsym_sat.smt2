; (str.to_re x)* = (str.to_re x)+ holds iff x empty; sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (= (re.* (str.to_re x)) (re.+ (str.to_re x))))
(check-sat)
