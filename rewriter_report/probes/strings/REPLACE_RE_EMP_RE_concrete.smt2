; replace_re nullable regex matches empty at 0
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_re "ba" (re.* (str.to_re "a")) "x") "xba")))
(check-sat)
