; replace_re_all nullable regex, empty matches skipped
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_re_all "ab" (re.* (str.to_re "a")) "x") "xb")))
(check-sat)
