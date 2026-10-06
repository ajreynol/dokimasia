; re.union(Sigma*a Sigma*, comp(a)) = all
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (str.in_re x (re.union (re.++ (re.* re.allchar) (str.to_re "a") (re.* re.allchar)) (re.comp (str.to_re "a"))))))
(check-sat)
