; inter: const str.to_re not in other component ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (str.to_re "ab") (re.* (str.to_re "a")))) (str.in_re x re.none))))
(check-sat)
