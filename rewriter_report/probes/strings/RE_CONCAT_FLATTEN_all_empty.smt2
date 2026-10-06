; re.++ of only empty-string regexes ---> str.to_re ""
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(assert (not (= (str.in_re x (re.++ (str.to_re "") (str.to_re ""))) (str.in_re x (str.to_re "")))))
(check-sat)
