; prefix ab vs regex prefix ac is a conflict
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "ab" x) (re.++ (str.to_re "ac") (re.* (str.to_re "c")))))
(check-sat)
