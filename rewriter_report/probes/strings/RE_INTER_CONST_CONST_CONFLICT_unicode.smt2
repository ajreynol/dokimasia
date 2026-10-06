; inter of \u{10000} and \u{ffff} constants ---> re.none
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.inter (str.to_re "\u{10000}") (str.to_re "\u{ffff}"))) (str.in_re x re.none))))
(check-sat)
