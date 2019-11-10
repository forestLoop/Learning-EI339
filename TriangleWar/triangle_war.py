__edges = ((1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 5), (3, 6), (4, 5), (5, 6), (4, 7), (4, 8), (5, 8), (5, 9), (6, 9), (6, 10), (7, 8), (8, 9), (9, 10))
edge_id = {edge: (1 << (idx + 1)) for idx, edge in enumerate(__edges)}
triangles = (14, 304, 104, 704, 68608, 6400, 143360, 25088, 311296)


def check_triangle(remaining_edges, edge):
    cnt = 0
    for t in triangles:
        if (t & edge) == 0:   # this triangle doesn't consist of this edge
            continue
        flag = True
        while t != 0:
            e = t & (-t)    # the lowest 1 bit in t, i.e., an edge that forms t
            if e in remaining_edges:    # this edge not added yet
                flag = False
                break
            t -= e
        cnt += 1 if flag else 0
    return cnt


def alpha_beta_search(remaining_edges, cnt_A, cnt_B, turn_A, alpha=-1, beta=1):
    if cnt_A >= 5:
        return 1
    elif cnt_B >= 5:
        return -1
    if turn_A:
        for e in remaining_edges:
            new_remain = {x for x in remaining_edges if x != e}
            cnt_diff = check_triangle(new_remain, e)
            if cnt_diff:
                alpha = max(alpha, alpha_beta_search(new_remain, cnt_A + cnt_diff, cnt_B,
                                                     turn_A, alpha, beta))
            else:
                alpha = max(alpha, alpha_beta_search(new_remain, cnt_A, cnt_B, not turn_A,
                                                     alpha, beta))
            if alpha >= beta:
                return beta
        return alpha
    else:
        for e in remaining_edges:
            new_remain = {x for x in remaining_edges if x != e}
            cnt_diff = check_triangle(new_remain, e)
            if cnt_diff:
                beta = min(beta, alpha_beta_search(new_remain, cnt_A, cnt_B + cnt_diff,
                                                   turn_A, alpha, beta))
            else:
                beta = min(beta, alpha_beta_search(new_remain, cnt_A, cnt_B, not turn_A,
                                                   alpha, beta))
            if alpha >= beta:
                return alpha
        return beta


def main():
    n = int(input("number of existing edges:"))
    assert 0 <= n <= 18, "Invalid input!"
    remaining_edges = set(edge_id.values())
    cnt_A, cnt_B = 0, 0
    turn_A = True
    for i in range(n):
        x, y = sorted(map(int, input().split()))
        edge = edge_id[(x, y)]
        remaining_edges.remove(edge)
        cnt_diff = check_triangle(remaining_edges, edge)
        if turn_A:
            cnt_A += cnt_diff
        else:
            cnt_B += cnt_diff
        turn_A = turn_A if cnt_diff else not turn_A
    res = alpha_beta_search(remaining_edges, cnt_A, cnt_B, turn_A)
    print("A" if res > 0 else "B", "wins.")


if __name__ == '__main__':
    while True:
        main()
