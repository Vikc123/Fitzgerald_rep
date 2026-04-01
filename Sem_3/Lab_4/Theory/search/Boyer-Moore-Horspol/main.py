def shift(pattern: str) -> "dict":
    table = {}
    for i in range(len(pattern)):
        table[pattern[i]] = len(pattern) - 1 - i
    return table

def boyer_moore_horspul(text: str, pattern: str) -> "int":
    t = len(text)
    p = len(pattern)
    shift_tabl = shift(pattern)
    i = 0
    while i <= t - p:
        j = p-1
        while j >= 0 and pattern[j] == text[i+j]:
            j -= 1
        if j < 0:
            return i
        i += shift_tabl.get(text[i+j], p)
    return -1



def main():
    text = "БОЛЬШИЕ МЕТЕО ДАННЫЕ"
    pattern = "ДАННЫЕ"
    print(boyer_moore_horspul(text, pattern))

if __name__ == "__main__":
    main()