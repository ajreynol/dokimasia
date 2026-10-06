; re.inter(a*, comp(Sigma*), R) = none
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.in_re x (re.inter (re.* (str.to_re "a")) (re.comp (re.* (re.union (str.to_re "a") (str.to_re "b")))) (re.* (str.to_re "c")))))
(check-sat)
