# def isMatch(s: str, p: str):
#     def hlpr(i, j):
#         if p[j] == ".":
#             return 1
#         else:
#             return 1 if s[i] == p[j] else 0
#
#     n = len(s)
#     m = len(p)
#     dp = [[] for _ in range(m)]
#     for i in range(m):
#         dp[i].extend([0 for _ in range(n)])
#
#     dp[0][0] = hlpr(0, 0)
#     last = 0
#
#     for i in range(1, m):
#         if last >= n:
#             break
#         dp[i][last] = dp[i - 1][last]
#
#         if p[i] == "*":
#             # dp[i][last] = 1
#             # if last < n - 1:
#             #     last += dp[i][last]
#             while last < n - 1:
#                 if value := dp[i][last] * hlpr(last + 1, i - 1):
#                     dp[i][last + 1] = value
#                     last += 1
#                 else:
#                     break
#         else:
#             if last == n - 1:
#                 if i < m - 1 and p[i + 1] == '*':
#                     continue
#                 if i == m - 1:
#                     dp[i][last] = hlpr(last, i)
#                     break
#             if (value := dp[i][last] * hlpr(last + 1, i)) == 0:
#                 dp[i][last + 1] = value
#                 last += 1 if p[i + 1] != "*" else 0
#             else:
#                 last += 1
#     for i in range(m):
#         print(dp[i])
#     return dp, dp[m - 1][n - 1]


def isMatch(s: str, p: str):
    def match_non_star(si, pi):
        return 1 if (p[pi] == "." or s[si] == p[pi]) else 0

    n = len(s) + 1
    m = len(p) + 1
    dp = [[] for _ in range(m)]
    for i in range(m):
        dp[i].extend([0 for _ in range(n)])

    dp[0][0] = 1

    for i in range(2, m):
        if p[i - 1] == '*':
            dp[i][0] = dp[i - 2][0]

    for i in range(m):
        print(dp[i])

    for i in range(1, m):
        for j in range(1, n):
            if p[i - 1] == '*':
                dp[i][j] = 1 if (dp[i - 2][j] or (match_non_star(j - 1, i - 1 - 1) and dp[i][j - 1])) else 0
            else:
                dp[i][j] = dp[i - 1][j - 1] * match_non_star(j - 1, i - 1)
    # for i in range(m):
    #     print(dp[i])
    return dp[m - 1][n - 1]


tests = [
    ("a", "ab*a", 1)
]

for s, p, r in tests:
    print(isMatch(s, p))
