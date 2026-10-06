; str.from_int of negative, zero, large
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const a String)(declare-const b String)(declare-const c String)
(assert (= a (str.from_int (- 5))))(assert (= b (str.from_int 0)))(assert (= c (str.from_int 123456789012345678901234567890)))
(assert (and (= a "") (= b "0") (= c "123456789012345678901234567890")))
(check-sat)
