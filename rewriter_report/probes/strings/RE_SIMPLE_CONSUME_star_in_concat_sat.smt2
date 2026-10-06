; a++x in a* ++ ab: x=ab sat, star must be repeat/skip correctly
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "a" x) (re.++ (re.* (str.to_re "a")) (str.to_re "ab"))))
(assert (not (str.in_re x (re.++ (re.* (str.to_re "a")) (str.to_re "ab")))))
(check-sat)
