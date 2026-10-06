; x++a++y in .*(a|b).* is true by inclusion
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (str.in_re (str.++ x "a" y) (re.++ (re.* re.allchar) (re.union (str.to_re "a") (str.to_re "b")) (re.* re.allchar)))))
(check-sat)
