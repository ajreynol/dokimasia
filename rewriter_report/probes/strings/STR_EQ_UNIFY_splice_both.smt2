; abc++x++de = ab++y++e  <=> c++x++d = y (prefix and suffix const splicing)
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "abc" x "de") (str.++ "ab" y "e")) (= (str.++ "c" x "d") y))))
(check-sat)
