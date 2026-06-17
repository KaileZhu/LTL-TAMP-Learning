import re

pattern = re.compile(r'\d+')  # 编译一个匹配数字的正则表达式
match = pattern.search('abc123def')  # 在字符串中查找匹配项

if match:
    print(match.group())  # 输出匹配到的数字
else:
    print('No match found')
