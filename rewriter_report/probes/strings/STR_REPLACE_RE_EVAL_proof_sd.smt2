; proof of replace_re evaluation with symbolic replacement
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= x "zabcz"))(assert (not (= (str.replace_re x (re.++ (str.to_re "a") (re.* re.allchar) (str.to_re "c")) y) (str.++ "z" y "z"))))
(check-sat)
