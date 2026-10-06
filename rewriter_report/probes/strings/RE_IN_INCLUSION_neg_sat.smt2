; x++a++y in _* b _* not included; x=y=empty falsifies
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (str.in_re (str.++ x "a" y) (re.++ (re.* re.allchar) (re.union (str.to_re "b") (str.to_re "c")) (re.* re.allchar)))))
(check-sat)
