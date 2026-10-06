; indexof_re constant evaluation incl. n=len, n>len, n<0, no match (z3 lacks str.indexof_re: ignore z3)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (and (= (str.indexof_re "zabcab" (re.++ (str.to_re "a") re.allchar) 2) 4) (= (str.indexof_re "abc" (str.to_re "") 3) 3) (= (str.indexof_re "abc" (str.to_re "") 4) (- 1)) (= (str.indexof_re "abc" re.allchar (- 1)) (- 1)) (= (str.indexof_re "abc" (str.to_re "d") 0) (- 1)))))
(check-sat)
