; re.++ with re.none ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (str.to_re "a") re.none (re.* (str.to_re "b")))) (str.in_re x re.none))))
(check-sat)
