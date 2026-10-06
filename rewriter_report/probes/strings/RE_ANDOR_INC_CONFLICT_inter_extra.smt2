; inter with extra child: (comp R1) R2 R3 ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (re.comp (re.++ (re.* re.allchar) (str.to_re "a") (re.* re.allchar))) (re.* (str.to_re "b")) (re.++ (str.to_re "a") (re.* re.allchar)))) (str.in_re x re.none))))
(check-sat)
