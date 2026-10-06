; x ++ a ++ from_int(n) in _* a [0-9]+ is not valid: n<0 gives empty digits
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const n Int)
(assert (not (str.in_re (str.++ x "a" (str.from_int n)) (re.++ (re.* re.allchar) (re.union (str.to_re "a") (str.to_re "b")) (re.range "0" "9") (re.* (re.range "0" "9"))))))
(check-sat)
