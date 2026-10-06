; str.<= on prefixes and code-point order
; EXPECT: sat
(set-logic QF_SLIA)
(assert (str.<= "ab" "abc"))(assert (not (str.<= "abc" "ab")))(assert (not (str.<= "b" "ab")))
(assert (str.<= "\u{0}" "\u{1}"))(assert (str.<= "Z" "a"))(assert (not (str.< "a" "a")))
(check-sat)
