; indexof_re evaluation on constants with non-nullable REs (start inside, beyond length, negative)
; EXPECT: unsat
(set-logic QF_SLIA)
(assert (not (and (= (str.indexof_re "zabcab" (re.++ (str.to_re "a") re.allchar) 2) 4) (= (str.indexof_re "zabcab" (re.++ (str.to_re "a") re.allchar) 0) 1) (= (str.indexof_re "abc" re.allchar 4) (- 1)) (= (str.indexof_re "abc" re.allchar (- 2)) (- 1)) (= (str.indexof_re "abc" (re.+ (re.range "b" "c")) 0) 1))))
(check-sat)
