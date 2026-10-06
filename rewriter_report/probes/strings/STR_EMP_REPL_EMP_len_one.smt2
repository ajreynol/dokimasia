; "" = replace(x,"a","") <=> prefixof(x,"a")
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= "" (str.replace x "a" "")) (str.prefixof x "a"))))
(check-sat)
