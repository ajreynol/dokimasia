; x = replace(x,"",b) <=> not contains(x,"") i.e. false
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= x (str.replace x "" "b")) false)))
(check-sat)
