; star of range followed by range
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (re.* (re.range "a" "c")) (re.range "a" "c"))) (str.in_re x (re.++ (re.range "a" "c") (re.* (re.range "a" "c")))))))
(check-sat)
