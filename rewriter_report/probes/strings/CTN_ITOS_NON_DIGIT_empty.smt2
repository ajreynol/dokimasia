; from_int with non-digit-free empty?
; EXPECT: sat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (str.contains (str.from_int n) ""))
(check-sat)
