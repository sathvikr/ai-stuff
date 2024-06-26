# for move in othello_imports.possible_moves(test_board, "x"):
#     child = othello_imports.make_move(test_board, "x", move)
#     print(move, evaluate(child))
#     othello_imports.nicely_print(child)

# results = []
#
# with open("boards_timing.txt") as f:
#     for line in f:
#         board, token = line.strip().split()
#         temp_list = [board, token]
#         print(temp_list)
#
#         for count in range(1, 7):
#             print("depth:", count)
#             start = time.perf_counter()
#             find_next_move(board, token, count)
#             end = time.perf_counter()
#             temp_list.append(str(end - start))
#
#         print(temp_list)
#         print()
#
#         results.append(temp_list)
#
# for line in results:
#     print(line)
