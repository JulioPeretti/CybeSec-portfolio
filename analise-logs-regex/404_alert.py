import re


def alert_check(server_log):

    with open(server_log, "r") as file:
        error_logs = {}
        for line in file:

            pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).* 404"
            actual_list = re.findall(pattern, line)

            if actual_list:

                attacker_ip = actual_list[0]

                if attacker_ip in error_logs:

                    error_logs[attacker_ip] += 1

                else:
                    error_logs[attacker_ip] = 1

    suspects_list = []

    for ip in error_logs:
        if error_logs[ip] >= 5:
            suspects_list.append(ip)

    with open("suspects_log.txt", "w") as file:
        suspects_string = "\n".join(suspects_list)
        suspects_file = file.write(suspects_string)

    return (suspects_string)


log_file = "server_log.txt"
print(alert_check(log_file))
