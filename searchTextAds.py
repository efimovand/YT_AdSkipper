

# Анализ текста на наличие рекламы
def findAds(strings_list):

    result = []

    triggers_A = ['описан', 'ссылка', 'промокод']
    triggers_B = ['скидк', 'бонус']
    triggers_C = ['хочу', 'рекоменд']

    keepChain_B = False
    keepChain_C = False

    for s in reversed(strings_list):

        s = s.lower()

        if any(word in s for word in triggers_A):
            result.append(s)
            keepChain_B = True
            keepChain_C = False

        elif any(word in s for word in triggers_B) and keepChain_B:
            result.append(s)
            keepChain_C = True

        elif any(word in s for word in triggers_C) and keepChain_C:
            result.append(s)

        else:
            keepChain_B = False
            keepChain_C = False

    result.reverse()
    return result