; re.loop 1 3 eliminated to union of concats
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re x ((_ re.loop 1 3) (str.to_re y))) (or (= x y) (= x (str.++ y y)) (= x (str.++ y y y))))))
(check-sat)
