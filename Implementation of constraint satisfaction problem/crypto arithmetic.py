from re import sub

def solve(q):
    try:
        n = (i for i in q if i.isalpha()).__next__()
    except StopIteration:
        return q if eval(sub(r'(^|[^0-9])0+([1-9]+)', r'\1\2', q)) else False
    else:
        for i in (str(i) for i in range(10) if str(i) not in q):
            res = solve(q.replace(n, str(i)))
            if res:
                return res
            return False
        
if __name__ == "__main__":
    query = str(input("Enter the String:"))
    r = solve(query)
    if r:
        print(r)
        for j in range(len(query)):
            print(query[j], "-->", r[j])
    else:
        print("Solution Not Found")