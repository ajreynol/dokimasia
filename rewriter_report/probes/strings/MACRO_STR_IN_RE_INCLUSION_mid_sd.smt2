; x++"ab"++y in Sigma*.b.Sigma*
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (str.in_re (str.++ x "ab" y) (re.++ (re.* re.allchar) (str.to_re "b") (re.* re.allchar)))))
(check-sat)
