def double(x):
    return x*2

seq = [1,2,3,4,5,6]

doubled = [(lambda x: x *2)(x) for x in seq]

print(doubled)

doubled2 = list(map(lambda x:x*2, seq))
print(doubled2)



