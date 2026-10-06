; str.to_code on empty, multi-char, max code point 196607, NUL
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const a Int)(declare-const b Int)(declare-const c Int)(declare-const d Int)
(assert (= a (str.to_code "")))(assert (= b (str.to_code "ab")))
(assert (= c (str.to_code "\u{2ffff}")))(assert (= d (str.to_code "\u{0}")))
(assert (and (= a (- 1)) (= b (- 1)) (= c 196607) (= d 0)))
(check-sat)
