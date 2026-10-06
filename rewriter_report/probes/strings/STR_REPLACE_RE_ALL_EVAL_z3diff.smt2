; differential: replace_re_all with star body; z3 comparison
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (= x (str.replace_re_all "aab" (re.* (str.to_re "a")) "X")))
(assert (not (= x "XXb")))
(check-sat)
