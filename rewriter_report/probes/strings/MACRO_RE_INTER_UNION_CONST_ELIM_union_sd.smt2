; re.union(str.to_re "aa", a*) behaves as a*
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re x (re.union (str.to_re "aa") (re.* (str.to_re "a")) (re.* (str.to_re "b")))) (str.in_re x (re.union (re.* (str.to_re "a")) (re.* (str.to_re "b")))))))
(check-sat)
