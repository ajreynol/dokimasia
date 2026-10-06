; contains("\u{10000}b", b++x++\u{10000}) ---> false
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (not (= (str.contains "\u{10000}b" (str.++ "b" x "\u{10000}")) false)))
(check-sat)
