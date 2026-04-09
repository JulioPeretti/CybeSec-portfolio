
def ip_check(allowed_file, blocked_file):

    with open(allowed_file, "r") as file:
        allowed_addresses = file.read()

    allowed_list = allowed_addresses.split("\n")

    with open(blocked_file, "r") as file:
        blocked_addresses = file.read()

    blocked_list = blocked_addresses.split("\n")

    new_allowed_list = []
    print(allowed_list)
    for i in allowed_list:
        if allowed_list.count(i) < 3 and i not in blocked_list and i not in new_allowed_list:
            print("The ip ", i, " passed the test and is allowed!")
            new_allowed_list.append(i)
        elif allowed_list.count(i) >= 3:
            print("The ip ", i, " had too many login tries and got blocked!")
        elif i in blocked_list:
            print("The ip ", i, " is in the blocked list and is not allowed!")
    print(new_allowed_list)
    with open(allowed_file, "w") as file:
        new_allowed_string = "\n".join(new_allowed_list)
        new_allowed_file = file.write(new_allowed_string)

    print("\n")
    return (new_allowed_string)


allowed_file = "CYBERSEC TASKS\\allow_list.txt"
blocked_file = "CYBERSEC TASKS\\remove_list.txt"

print(ip_check(allowed_file, blocked_file))
