import functools

white_moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
black_moves = ((-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2))


@functools.lru_cache(None)
def rounds_to_win(n, r1, c1, r2, c2, rounds, white_turn):
    if (r1, c1) == (r2, c2):
        return 0
    elif white_turn and ((r1 == r2 and abs(c1 - c2) <= 1) or (c1 == c2 and abs(r1 - r2) <= 1)):
        return 201920192019  # black will lose, so penalize this case
    elif not white_turn and ((r1 == r2 and abs(c1 - c2) <= 2) or (c1 == c2 and abs(r1 - r2) <= 2)):
        return 1
    elif rounds <= 0:   # make sure that the recursion depth is limited
        return 0
    if white_turn:
        return 1 + max(rounds_to_win(n, r1 + dr, c1 + dc, r2, c2, rounds - 1, False) for dr, dc in white_moves if 1 <= r1 + dr <= n and 1 <= c1 + dc <= n)
    else:
        return 1 + min(rounds_to_win(n, r1, c1, r2 + dr, c2 + dc, rounds - 1, True) for dr, dc in black_moves if 1 <= r2 + dr <= n and 1 <= c2 + dc <= n)


def solve(n, r1, c1, r2, c2):
    print("Round {:02d}:".format(0), (r1, c1), (r2, c2))
    if (r1 == r2 and abs(c1 - c2) == 1) or (c1 == c2 and abs(r1 - r2) == 1):
        print("WHITE 1")
        return
    # White is doomed to lose
    max_round = 4 * n
    white_turn = True
    for i in range(1, max_round + 1):
        if white_turn:
            white_pos = [(r1 + dr, c1 + dc) for dr, dc in white_moves if 1 <= r1 + dr <= n and 1 <= c1 + dc <= n]
            remaining_rounds = [rounds_to_win(n, new_r1, new_c1, r2, c2, max_round - i, False) for new_r1, new_c1 in white_pos]
            # print("White Pos:", white_pos, remaining_rounds)
            r1, c1 = white_pos[max(range(0, len(white_pos)), key=lambda x: remaining_rounds[x])]
        else:
            black_pos = [(r2 + dr, c2 + dc) for dr, dc in black_moves if 1 <= r2 + dr <= n and 1 <= c2 + dc <= n]
            remaining_rounds = [rounds_to_win(n, r1, c1, new_r2, new_c2, max_round - i, True) for new_r2, new_c2 in black_pos]
            # print("Black Pos:", black_pos, remaining_rounds)
            r2, c2 = black_pos[min(range(0, len(black_pos)), key=lambda x: remaining_rounds[x])]
        if (r1, c1) == (r2, c2):    # game ends
            print("WHITE" if white_turn else "BLACK", i)
            return
        print("Round {:02d}:".format(i), (r1, c1), (r2, c2))
        white_turn = not white_turn
    raise "Unsolved!"


if __name__ == '__main__':
    while True:
        try:
            n, r1, c1, r2, c2 = map(int, input("Please input n r1 c1 r2 c2:\n").split())
            assert 2 <= n <= 20, "2 <= n <= 20 is not satisfied!"
            assert all(1 <= x <= n for x in (r1, c1, r2, c2)), "1 <= ci, ri <= n is not satisfied!"
            assert (r1, c1) != (r2, c2), "(r1, c1) == (r2, c2)"
        except Exception as e:
            print("Error:", e, '\n')
            continue
        solve(n, r1, c1, r2, c2)
