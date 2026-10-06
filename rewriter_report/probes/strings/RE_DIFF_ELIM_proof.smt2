; re.diff eliminated to inter/comp
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.diff (re.* (re.range "a" "c")) (str.to_re y))) (str.in_re x (re.inter (re.* (re.range "a" "c")) (re.comp (str.to_re y)))))))
(check-sat)
