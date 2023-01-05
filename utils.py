def print_progress(index, total, fi="", last=""):
    percent = ("{0:.1f}").format(100 * ((index) / total))
    fill = int(30 * (index / total))
    spec_char = ["\x1b[1;36;40m━\x1b[0m", "\x1b[1;37;40m━\x1b[0m"]
    bar = spec_char[0]*fill + spec_char[1]*(30-fill)

    percent = " "*(5-len(str(percent))) + str(percent)

    if index == total:
        print("", end="\r")
        print(fi + " " + bar + " " + percent + "% " + last)
    else:
        print("", end="\r")
        print(fi + " " + bar + " " + percent + "% " + last, end="")