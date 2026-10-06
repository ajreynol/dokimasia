; "ab"++x in (ab)*.a does not reduce to false
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.in_re (str.++ "ab" x) (re.++ (re.* (str.to_re "ab")) (str.to_re "a"))))
(check-sat)
