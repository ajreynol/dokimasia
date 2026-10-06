; sequence version of split ctn: middle unit 3 vs pattern [1,2]
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(declare-const s (Seq Int))
(declare-const t (Seq Int))
(assert (not (= (seq.contains (seq.++ s (seq.unit 3) t) (seq.++ (seq.unit 1) (seq.unit 2))) (or (seq.contains s (seq.++ (seq.unit 1) (seq.unit 2))) (seq.contains t (seq.++ (seq.unit 1) (seq.unit 2)))))))
(check-sat)
