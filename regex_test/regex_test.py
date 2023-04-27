import re

RAW_STRING_1 = "2023-02-16 13_00_00.000.mp4"
RAW_STRING_2 = "2023-02-16_13_00_00.000.mp4"

def test_regex(string: str) -> list:
    pattern = re.compile(
        r"""                        
            (?P<year>\d+)[-] #()로 묶으면 그룹핑 - 해당 안쪽 식만 가져옴 
            (?P<month>\d+)[-]
            (?P<day>\d+)[\s|_]+
            (?P<hour>\d{2})[_]      # \d 는 숫자를 찾아라 {2} 는 2번 반복한다 
            (?P<minute>\d+)[_]    # ?P<별명> 으로 이름 설정 가능 
            (?P<second>\d+)[.]
            (?P<micro>\d+). # 정규식에서 . 은 기본적으로 dot 연산 (모든 값에 대응)그렇기 떄문에 []로 묶어서 인식
        """
    , re.VERBOSE) 
    searched_string = pattern.search(string)
    splited_string = list(map(int,
        [
        searched_string.group("year"),
        searched_string.group("month"),
        searched_string.group("day"),
        searched_string.group("hour"),
        searched_string.group("minute"),
        searched_string.group("second"),
        1000 * int(searched_string.group("micro"))
        ]))
    return splited_string


print(*test_regex(RAW_STRING_1), sep="\n")
print(*test_regex(RAW_STRING_2), sep="\n")