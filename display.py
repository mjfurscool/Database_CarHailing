import	sqlite3


def display(rows):
    l = len(rows)
    if(l == 0):
        print("There is nothing to show")
        return
    i = 0
    m = 0
    if l <= 5:
        for row in rows:
            print(row)

    else:
        while (l > 5):
            m += 5
            for row in range(i, m):
                print(rows[row])
            l -= 5
            i += 5
            if l > 5:
                se = str(input("see more?"))
                if (se != "y" and se != "Y"):
                    break
            elif (l<=5 and l>0):
                if se == "y" or se == "Y" and l > 0:
                    se = str(input("see more??"))
                    if (se == "y" or se == "Y"):
                        for row in range(m, len(rows)):
                            print(rows[row])
                        break
            else:
                break

    return