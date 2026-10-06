; consume constant suffix ba through range/allchar
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re (str.++ x "ba") (re.++ (re.* (str.to_re "c")) (re.range "a" "b") re.allchar)) (str.in_re x (re.* (str.to_re "c"))))))
(check-sat)
