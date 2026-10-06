; rev distributes over concat
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.rev (str.++ x "ab" y)) (str.++ (str.rev y) "ba" (str.rev x)))))
(check-sat)
