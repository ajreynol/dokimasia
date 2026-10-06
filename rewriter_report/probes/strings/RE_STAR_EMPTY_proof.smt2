; (re.none)* ---> ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.* re.none)) (str.in_re x (str.to_re "")))))
(check-sat)
