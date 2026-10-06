; x++ab in _* [a-c][a-c] by inclusion
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re (str.++ x "ab" y) (re.++ (re.* re.allchar) (re.range "a" "c") (re.range "a" "c") (re.* re.allchar))) true)))
(check-sat)
