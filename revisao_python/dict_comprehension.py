users = [
    (0,"Bob","pass"),
    (1,"Rolf","rof123"),
    (2,"Jose","jose456789"),
    (3,"user","user123")
]

# Uso do Dict Comprehension
username_mapping = {user[1] : user for user in users}

print(username_mapping)

username_input = input("Enter your username: ")
pass_input = input("Enter your password: ")

# Unpacking a tupla do dicionario
#_ : siginifica uma variavel que não tera importancia
_, username, password = username_mapping[username_input]

