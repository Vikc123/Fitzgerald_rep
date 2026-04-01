from moduls import Bohr

def main():
    dictionary = ['he', 'she', 'his', 'hers']
    ALPHA = 26
    t = Bohr.Trie(ALPHA)
    for s in dictionary:
        t.add(s)
    print(t.size())
    for s in  dictionary:
        print(t.find(s))
    print(t.find('se'), t.find('hi'))

    text = 'aalkflaldlheaddjhedlsflskdlja'
    v = t.root
    for i in range(len(text)):
        v = t.go(v, text[i])
        if v.is_terminal:
            print(i)
            print(text[i-3:i+1])


if __name__ == "__main__":
    main()