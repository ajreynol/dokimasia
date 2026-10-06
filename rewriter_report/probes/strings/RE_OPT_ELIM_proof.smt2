; re.opt eliminated to union with empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.opt (str.to_re y))) (str.in_re x (re.union (str.to_re "") (str.to_re y))))))
(check-sat)
