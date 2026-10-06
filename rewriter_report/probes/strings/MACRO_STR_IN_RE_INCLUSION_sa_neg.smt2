; x++a++y in .*b.* is not valid
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (str.in_re (str.++ x "a" y) (re.++ (re.* re.allchar) (str.to_re "b") (re.* re.allchar)))))
(check-sat)
