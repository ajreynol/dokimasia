; contains(x++y++ab, y++a) ---> true (const suffix/prefix splitting)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains (str.++ x y "ab") (str.++ y "a")) true)))
(check-sat)
