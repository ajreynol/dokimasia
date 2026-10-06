; _* "a" _ _* is not contains (allchar present): x=a sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (= x "a"))
(assert (not (str.in_re x (re.++ (re.* re.allchar) (str.to_re "a") re.allchar (re.* re.allchar)))))
(check-sat)
