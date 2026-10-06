; indexof_re edge cases (n=len with nullable re, n>len, n<0, empty s). z3 lacks str.indexof_re: its answer is not evidence
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (and (= (str.indexof_re "ab" (re.* (str.to_re "z")) 2) 2) (= (str.indexof_re "ab" (re.* (str.to_re "z")) 3) (- 1)) (= (str.indexof_re "ab" (re.* (str.to_re "z")) (- 1)) (- 1)) (= (str.indexof_re "" (str.to_re "a") 0) (- 1)))))
(check-sat)
