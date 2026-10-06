; ab++x in inter((a.)*, (.b)*) with x=ab sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "ab" x) (re.inter (re.* (re.++ (str.to_re "a") re.allchar)) (re.* (re.++ re.allchar (str.to_re "b"))))))
(assert (not (= x "")))
(check-sat)
