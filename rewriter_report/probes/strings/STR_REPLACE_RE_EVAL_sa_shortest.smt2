; replace_re picks leftmost shortest match: ZABCZACZ, A.*C, y -> Z y ZACZ
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.replace_re "ZABCZACZ" (re.++ (str.to_re "A") (re.* re.allchar) (str.to_re "C")) y) (str.++ "Z" y "ZACZ"))))
(check-sat)
