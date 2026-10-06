; re.loop 0 2 includes empty
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re x ((_ re.loop 0 2) (re.range "a" "b"))) (or (= x "") (str.in_re x (re.range "a" "b")) (str.in_re x (re.++ (re.range "a" "b") (re.range "a" "b")))))))
(check-sat)
