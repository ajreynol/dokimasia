; x++y in (ab)* is NOT the conjunction (length-2 elements)
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.in_re (str.++ x y) (re.* (str.to_re "ab"))) (and (str.in_re x (re.* (str.to_re "ab"))) (str.in_re y (re.* (str.to_re "ab")))))))
(check-sat)
