import sys

sys.path.append("..")
from src.nq.test import add_some, get_bjd_df
from src.nq.hwp import hwp_to_xmlstr
from src.nq.vid import formatFloat, generateRegistrationVid
from src.nq.data import getData
from src.nq.pnu import getBjd, getRegionCode
from src.nq.sql import constr

from pandas import read_sql

add_two = add_some(2)
print(add_two(3))


print(hwp_to_xmlstr("서울특별시 도시계획 조례(서울특별시조례)(제8186호)(20210930).hwp")[:1000])
print(
    hwp_to_xmlstr(
        "[별표 2] 제1종전용주거지역안에서 건축할 수 있는 건축물(제71조제1항제1호관련)(국토의 계획 및 이용에 관한 법률 시행령).hwp"
    )[:1000]
)

print(formatFloat(123))
print(formatFloat(12300))
print(formatFloat(12300.00))
print(formatFloat(12300.01))
print(formatFloat(12300.010))

print(generateRegistrationVid("1168010600109450010", "20220601", 1))
print(generateRegistrationVid("1168010600109450010", "20220601", 1))
print(
    generateRegistrationVid(
        "1168010600109450010", "20220601", "1312300.00", "123.56", "234.4", "농심", "농협"
    )
)
print(
    generateRegistrationVid(
        "1168010600109450010", "20220601", "1312300.00", "-", "234.4", "농심", "농협"
    )
)
print(generateRegistrationVid("1168010600109450010", "20220601", "1312300.00.0"))
print(generateRegistrationVid("1168010600109450010", "20220640", 1))
print(generateRegistrationVid("1168010600109450010a", "111", 1))
print(generateRegistrationVid("a1168010600109450010", "111", 1))
print(generateRegistrationVid("1a68010600109450010", "111", 1))
print(generateRegistrationVid("111", "111", 1))

# print(get_bjd_df())

# print(getBjd("1168010600"))
# print(getBjd(1168010600))
# print(getBjd(3611031025))
# print(getBjd(3611031026))

# print(getBjd(1168010600, def_date="20220401"))
# print(getBjd(3611031025, def_date="20220401"))
# print(getBjd(3611031026, def_date="20220401"))

# print(getRegionCode("울산광역시 울주군 삼남읍 교동리"))
# print(getRegionCode("충청북도 청주시 상당구 북문로1가동"))
# print(getRegionCode("강원도 횡성군 횡성읍 청룡리"))
print(getRegionCode("경기도 광주시 고산동"))

# print(getRegionCode("울산광역시 울주군 삼남읍 교동리", def_date="20220401"))
# print(getRegionCode("충청북도 청주시 상당구 북문로1가동", def_date="20220401"))
# print(getRegionCode("강원도 횡성군 횡성읍 청룡리", def_date="20220401"))
print(getRegionCode("경기도 광주시 고산동", def_date="20220401"))

print(constr(envfile=".db_env"))
print(constr(host="localhost", port=5432))
print(constr())

print(read_sql("select 1 as num", con=constr(envfile=".env")))
