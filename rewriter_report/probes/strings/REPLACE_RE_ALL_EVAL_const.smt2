; replace_re_all evaluation
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_re_all "baaab" (re.+ (str.to_re "a")) "x") "bxxxb")))
(check-sat)
