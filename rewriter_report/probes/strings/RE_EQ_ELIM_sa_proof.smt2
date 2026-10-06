; regex equality a* = (eps | a a*) is valid, so its negation is unsat
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (re.* (str.to_re "a")) (re.union (str.to_re "") (re.++ (str.to_re "a") (re.* (str.to_re "a")))))))
(check-sat)
