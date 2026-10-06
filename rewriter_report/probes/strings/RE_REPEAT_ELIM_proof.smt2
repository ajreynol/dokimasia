; re.^ 3 eliminated to re.loop 3 3
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x ((_ re.^ 3) (str.to_re y))) (str.in_re x ((_ re.loop 3 3) (str.to_re y))))))
(check-sat)
