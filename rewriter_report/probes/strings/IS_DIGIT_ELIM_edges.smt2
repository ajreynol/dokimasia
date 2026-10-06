; is_digit on empty, 2-char, '/', ':', '0', '9'
; EXPECT: sat
(set-logic QF_SLIA)
(assert (not (str.is_digit "")))(assert (not (str.is_digit "10")))(assert (not (str.is_digit "/")))
(assert (not (str.is_digit ":")))(assert (str.is_digit "0"))(assert (str.is_digit "9"))
(check-sat)
