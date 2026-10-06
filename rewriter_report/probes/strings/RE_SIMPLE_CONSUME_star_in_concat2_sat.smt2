; a++x in a* ++ b ++ x-indep: x=b sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "a" x) (re.++ (re.* (str.to_re "a")) (str.to_re "b") (re.* re.allchar))))
(assert (= (str.len x) 1))
(check-sat)
