; membership in 3-ary union is disjunction
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.union (str.to_re y) (str.to_re z) (re.* (str.to_re "a")))) (or (= x y) (= x z) (str.in_re x (re.* (str.to_re "a")))))))
(check-sat)
