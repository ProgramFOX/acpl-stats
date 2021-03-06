from pgnreader import annotation_to_cp, acpl_white_black
from pgnreader_median import mcpl_white_black
from pgnreader_qop import qop_white_black
from pgnreader_winningchances import awcpl_white_black

assert annotation_to_cp("-0.2") == -20
assert annotation_to_cp("1.4") == 140
assert annotation_to_cp("-11.77") == -1000
assert annotation_to_cp("53.89") == 1000
assert annotation_to_cp("#-5") == -1000
assert annotation_to_cp("#2") == 1000

pgn1 = "1. e4 { [%eval 0.2] } 1... e6 { [%eval 0.13] } 2. Bc4 { [%eval -0.31] } 2... d5 { [%eval -0.28] } 3. exd5 { [%eval -0.37] } 3... exd5 { [%eval -0.31] } 4. Bb3 { [%eval -0.33] } 4... Nf6 { [%eval -0.35] } 5. d4 { [%eval -0.34] } 5... Be7 { [%eval 0.0] } 6. Nf3 { [%eval 0.0] } 6... O-O { [%eval -0.08] } 7. Bg5 { [%eval -0.19] } 7... h6 { [%eval -0.29] } 8. Bxf6 { [%eval -0.36] } 8... Bxf6 { [%eval -0.37] } 9. O-O { [%eval -0.36] } 9... c6 { [%eval -0.12] } 10. Re1 { [%eval -0.17] } 10... Bf5 { [%eval -0.04] } 11. c4?! { [%eval -0.67] } 11... dxc4 { [%eval -0.5] } 12. Bxc4 { [%eval -0.77] } 12... Nd7?! { [%eval -0.1] } 13. Nc3 { [%eval 0.0] } 13... Nb6 { [%eval 0.0] } 14. b3?! { [%eval -0.76] } 14... Nxc4 { [%eval -0.49] } 15. bxc4 { [%eval -0.65] } 15... Qa5 { [%eval -0.55] } 16. Rc1 { [%eval -0.79] } 16... Rad8 { [%eval -0.78] } 17. d5?? { [%eval -5.41] } 17... Bxc3 { [%eval -5.42] } 18. Re5? { [%eval -7.61] } 18... Bxe5 { [%eval -7.78] } 19. Nxe5 { [%eval -7.72] } 19... cxd5 { [%eval -7.81] } 20. Qe1? { [%eval -9.29] } 20... Be6?? { [%eval 3.71] } 21. Rd1?? { [%eval -12.34] } 21... dxc4 { [%eval -12.71] } 22. Rxd8?! { [%eval #-1] } 22... Rxd8?! { [%eval -13.06] } 23. Qc3?! { [%eval #-2] } 23... Qxc3?! { [%eval #-4] } 24. g3 { [%eval #-3] } 24... Rd1+?! { [%eval #-4] } 25. Kg2 { [%eval #-4] } 25... Qe1?! { [%eval #-4] } 26. Kf3 { [%eval #-3] } 26... Qxe5 { [%eval #-2] } 27. Kg2 { [%eval #-2] } 27... Bd5+?! { [%eval #-2] } 28. Kh3 { [%eval #-1] } 28... Qh5# 0-1"
assert acpl_white_black(pgn1) == (88, 55)
pgn2 = "1. e4 { [%eval 0.12] } 1... e5 { [%eval 0.26] } 2. Nf3 { [%eval 0.21] } 2... d6 { [%eval 0.3] } 3. d4 { [%eval 0.35] } 3... exd4 { [%eval 0.34] } 4. Nxd4 { [%eval 0.3] } 4... Nf6 { [%eval 0.41] } 5. Nc3 { [%eval 0.35] } 5... Be7 { [%eval 0.33] } 6. Be3 { [%eval 0.2] } 6... O-O { [%eval 0.16] } 7. Be2 { [%eval 0.18] } 7... Nbd7 { [%eval 0.41] } 8. Qd2 { [%eval 0.17] } 8... Nc5 { [%eval 0.61] } 9. f3 { [%eval 0.58] } 9... Nfd7 { [%eval 0.94] } 10. O-O-O { [%eval 0.97] } 10... Ne6 { [%eval 1.06] } 11. Kb1 { [%eval 0.79] } 11... Nxd4 { [%eval 0.81] } 12. Bxd4 { [%eval 0.48] } 12... Nb6?! { [%eval 1.11] } 13. g4 { [%eval 1.03] } 13... Be6 { [%eval 1.05] } 14. h4 { [%eval 1.13] } 14... Bxh4 { [%eval 2.29] } 15. f4?! { [%eval 1.36] } 15... Bc4? { [%eval 3.99] } 16. Bxc4 { [%eval 3.63] } 16... Nxc4 { [%eval 4.06] } 17. Qd3 { [%eval 3.72] } 17... c5 { [%eval 3.74] } 18. Qxc4? { [%eval 2.22] } 18... cxd4 { [%eval 2.64] } 19. Rxd4?! { [%eval 2.0] } 19... Rc8? { [%eval 3.7] } 20. Qd3 { [%eval 3.43] } 20... Bf6?? { [%eval 6.97] } 21. e5 { [%eval 6.93] } 21... Be7?? { [%eval #1] } 22. Qxh7# 1-0"
assert acpl_white_black(pgn2) == (25, 71)

assert mcpl_white_black(pgn1) == (3, 0)
assert mcpl_white_black(pgn2) == (8, 23)

assert qop_white_black(pgn1) == (71, 79)

print("Tests passed!")