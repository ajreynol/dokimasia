; "abab" in (ab)* true; "aba" false
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= x "abab"))(assert (= y "aba"))(assert (or (not (str.in_re x (re.* (str.to_re "ab")))) (str.in_re y (re.* (str.to_re "ab")))))
(check-sat)
