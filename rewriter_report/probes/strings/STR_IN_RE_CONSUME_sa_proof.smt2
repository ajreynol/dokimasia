; consume constant prefix/suffix: ab++x++c in a.*d is false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (str.in_re (str.++ "ab" x "c") (re.++ (str.to_re "a") (re.* re.allchar) (str.to_re "d"))))
(check-sat)
