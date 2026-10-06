; str.from_code at -1, 0, 196607, 196608
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const a String)(declare-const b String)(declare-const c String)(declare-const d String)
(assert (= a (str.from_code (- 1))))(assert (= b (str.from_code 0)))
(assert (= c (str.from_code 196607)))(assert (= d (str.from_code 196608)))
(assert (and (= a "") (= b "\u{0}") (= c "\u{2ffff}") (= d "")))
(check-sat)
