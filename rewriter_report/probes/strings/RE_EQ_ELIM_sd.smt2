; equality of regexes a* = (aa)*.a? is decided via forall
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (re.* (str.to_re "a")) (re.++ (re.* (str.to_re "aa")) (re.opt (str.to_re "a"))))))
(check-sat)
