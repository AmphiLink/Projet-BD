ma_liste = []


def test_function(ma_liste):
    print(ma_liste)
    a = 1
    ma_liste = [1, 2, 3, 4, 5]
    print(ma_liste)
    return test_function()


test_function(ma_liste)
