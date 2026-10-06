; membership edge cases: empty string in comp(empty), range bounds, max char
; EXPECT: sat
(set-logic ALL)
(assert (str.in_re "" (re.comp (re.+ re.allchar))))(assert (str.in_re "\u{2ffff}" re.allchar))(assert (not (str.in_re "ab" (re.range "a" "b"))))(assert (str.in_re "b" (re.range "a" "b")))(assert (not (str.in_re "a" (re.range "b" "a"))))(assert (not (str.in_re "a" (re.range "ab" "c"))))
(check-sat)
