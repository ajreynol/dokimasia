; x ++ from_int(n) in _* [0-9]* holds by generalized-const inclusion (from_int over-approximated by digit star)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const n Int)
(assert (not (str.in_re (str.++ x "a" (str.from_int n)) (re.++ (re.* re.allchar) (re.union (str.to_re "a") (str.to_re "b")) (re.* (re.range "0" "9"))))))
(check-sat)
