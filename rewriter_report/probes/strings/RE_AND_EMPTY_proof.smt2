; re.inter with re.none ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (re.* (str.to_re "a")) re.none)) (str.in_re x re.none))))
(check-sat)
