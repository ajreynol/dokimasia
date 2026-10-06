; re.inter(str.to_re "aa", a*, Sigma*b?) -> conflict/none or const
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.in_re x (re.inter (str.to_re "aa") (re.* (str.to_re "b")))))
(check-sat)
