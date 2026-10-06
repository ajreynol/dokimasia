; membership in 3-ary inter is conjunction
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.inter (re.* (str.to_re y)) (re.* (str.to_re z)) (re.* (str.to_re "a")))) (and (str.in_re x (re.* (str.to_re y))) (str.in_re x (re.* (str.to_re z))) (str.in_re x (re.* (str.to_re "a")))))))
(check-sat)
