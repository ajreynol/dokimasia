; re.inter(str.to_re "ab", a.Sigma*, Sigma*.b) = str.to_re "ab"
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re x (re.inter (str.to_re "ab") (re.++ (str.to_re "a") (re.* re.allchar)) (re.++ (re.* re.allchar) (str.to_re "b")))) (= x "ab"))))
(check-sat)
