; to_lower(to_upper x) = to_lower x and to_upper(to_upper x) = to_upper x
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(assert (or (not (= (str.to_lower (str.to_upper x)) (str.to_lower x)))
            (not (= (str.to_upper (str.to_upper x)) (str.to_upper x)))))
(check-sat)
