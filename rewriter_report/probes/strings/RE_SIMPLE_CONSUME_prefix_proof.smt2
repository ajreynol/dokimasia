; consume constant prefix ab from x-membership
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.in_re (str.++ "ab" x) (re.++ (str.to_re "ab") (re.* (str.to_re "c")))) (str.in_re x (re.* (str.to_re "c"))))))
(check-sat)
