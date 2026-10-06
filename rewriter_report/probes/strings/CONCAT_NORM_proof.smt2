; nested concat flattening, constant merging, empty removal
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const u String)
(assert (not (= (str.++ (str.++ x "a") "" (str.++ "b" y) "c") (str.++ x "ab" y "c"))))
(check-sat)
