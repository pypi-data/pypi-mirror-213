from max import Max

val = {
    "A": 20,
    "B":30,
    "C":10
}
val2 = (2,3,42,3,44,3,2,1)
result = Max.max_num_dict(val)
# for (a,b) in result.items():
#     print(f"{a} got the highest mark: {b}")
result2 = Max.max_num_list(val2)
print(result2)