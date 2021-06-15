import random as rd
preword = [
   "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ",
   "ㅈ", "ㅉ", "ㅊ", "ㅋ","ㅌ", "ㅍ", "ㅎ"]

inword = [
   "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ",
   "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]

postword = [
   "", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ",
   "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ",
   "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

totlist = list()

def ranword():
    totlist.clear()
    for i in range(rd.randint(1,5)):
        w1, w2, w3 = rd.randint(0, len(preword) - 1), rd.randint(0, len(inword) - 1), rd.randint(0, len(postword) - 1)
        totlist.append(chr(0xAC00 + ((w1*21)+w2)*28+w3))
    return "".join(totlist)
