; str.to_int of empty, leading zeros, minus sign, space, non-digit
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const a Int)(declare-const b Int)(declare-const c Int)(declare-const d Int)(declare-const e Int)
(assert (= a (str.to_int "")))(assert (= b (str.to_int "007")))(assert (= c (str.to_int "-1")))
(assert (= d (str.to_int " 1")))(assert (= e (str.to_int "00000000000000000000123456789012345678901234567890")))
(assert (and (= a (- 1)) (= b 7) (= c (- 1)) (= d (- 1)) (= e 123456789012345678901234567890)))
(check-sat)
