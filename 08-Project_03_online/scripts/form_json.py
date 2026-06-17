import json

weapons = {
    "success": True,
    "message": "成功",
    "code": 200,
    "result": [
        {
            "id": None,
            "createBy": "admin",
            "createTime": "2024-04-29 17:55:03",
            "updateBy": "admin",
            "updateTime": "2024-05-13 18:55:05",
            "sysOrgCode": "A01",
            "zbbs": "fscbs007",   #车标识
            "zbnm": "fscnm007",   #车内码
            "zbmc": "17",         #车名称
            "zbjc": "",
            "ptlx": "PTLXNM001",  #平台类型内码
            "xdzl": 1,
            "cllxnm": "CLLXNM002",
            "zzwqxhnm": "zzwqxhnm001", #装载weapon型号内码
            "sfky": "是",
            "zdblxnm": "ZDBLXNM001",  #zdb类型
            "lsbdnm": "bd006102",
            "lszqnm": "ZQNM001",
            "lsjqnm": "jq001",
            "lszzqnm": "zzq6102001",
            "lszbgcnm": "zbgc6102001001",
            "ms": "",
            "jsztnm": 'rdj',
            "rwztnm": None,
            "rwbh": None,
            "rwjl": None,
            "jkzt": None,
            "xdsl": 2,    #携d数量
            "wd": None,   #纬度
            "jd": None,   #经度
            "gc": None,   #高程
            "sd": None,
            "nlzt": None,
            "sbbs": None,
            "sbsj": None,
            "sbzyip": None,
            "sbzydk": None,
            "bdglip": None,
            "bdgldk": None
        }
    ],
    "timestamp": 1715910355715
}

targets = {
  "success": True,
  "message": "成功",
  "code": 200,
  "result": [
    {
      "id": None,
      "createBy": None,
      "createTime": None,
      "updateBy": None,
      "updateTime": None,
      "sysOrgCode": None,
      "mbbs": "36",  #目标标识
      "mbbh": None,
      "mblx": "MBLX002", #类型内码
      "mbmc": None,
      "mbhs": 17, 
      "mbhx": None,
      "mbzt": None,
      "ssgj": None,
      "wd": "22.81221", #经度
      "jd": "131.55465", #纬度
      "gc": None, #高程
      "dzmbxhnm": None,
      "rwbh": None,
      "pcbh": "001",
      "zynm": None,
      "mbwc": None,
      "zyzcsj": "2024-05-24 16:25:26", #侦察获取时间
      "khnl": None,
      "js": None,
      "zzqybh": None,
      "rwbs": "551b7c7fce814730835a2da0418be57d", #任务标识
      "pcbs": None
    },
    {
      "id": None,
      "createBy": None,
      "createTime": None,
      "updateBy": None,
      "updateTime": None,
      "sysOrgCode": None,
      "mbbs": "37",
      "mbbh": None,
      "mblx": "MBLX002",
      "mbmc": None,
      "mbhs": 17,
      "mbhx": None,
      "mbzt": None,
      "ssgj": None,
      "wd": "21.8112",
      "jd": "132.5475",
      "gc": None,
      "dzmbxhnm": None,
      "rwbh": None,
      "pcbh": "001",
      "zynm": None,
      "mbwc": None,
      "zyzcsj": "2024-05-24 16:25:26",
      "khnl": None,
      "js": None,
      "zzqybh": None,
      "rwbs": "551b7c7fce814730835a2da0418be57d",
      "pcbs": None
    }
  ],
  "timestamp": 1716546049564
}


ssl_list = {
    "result": [
        {
            "RWBS": "",  #任务标识
            "SSLBS": "fscbs007-ssl0",  #ssl标识
            "sslmc": "fscnm007-ssl0",  #ssl名称 #没了
            "MBBS": "", #目标标识
            "ZCPTBS": "", #ZC平台标识
            "ZCKSSJ": "2024-04-29 17:55:03",
            "ZCJSSJ": "2024-04-29 17:55:03",
            "ZHPTBS": "", #zh平台标识
            "HLPTBS": "", #hl平台标识（对应weapon车标识）
            "XDSL": 2, #携D数量
            "DJZZSJ": "2024-04-29 17:55:03", #最早开始时间
            "DJZWSJ": "2024-04-29 17:55:03", #最晚开始时间
            "MZZZSJ": "2024-04-29 17:55:03", #最早完成时间
            "MZZWSJ": "2024-04-29 17:55:03", #最晚结束时间
            "DJBHSJ": 200,    #执行时间
            "DJJDYQ": 0.99     #精度预期
        }
    ]
}

yapg = {

    "result": [
        {
            "rwbs": "task001",
            "ssyabs": "fscbs001", #预案标识
            "ssyamc": "fscnm001", #预案名称
            "yazsc": 1000, #预案总时长
            "yadjjd": 0.99, #预案精度
            "yarwwcd": 0.99, #成功率
            "yafxdj": 0.99, #风险等级（暂时1-成功率吧）
            "yacb": 2800 #预案成本
        }
    ]
}

dlgh = { 

    "result": [
        {
            "rwbs": "task001",
            "mbbs": "mbbs001", #对应目标(多余/删掉)
            "ssyabs": "ssyabs001", #对应预案
            "ssyamx": [   #对应预案明细
                {
                    "mbbs": "mbbs001", #目标标识
                    "yxj": 1,   #优先级
                    "dxdl":[
                        {
                            "zzwqxhnm": "zzwqxhnm001", #需要weapon型号内码
                            "zdblxnm": "ZDBLXNM001",  #zdb类型
                            "dl": 2,    #数量
                        },
                        {
                            "zzwqxhnm": "zzwqxhnm002", #需要weapon型号内码
                            "zdblxnm": "ZDBLXNM002",  #zdb类型
                            "dl": 2,    #数量
                        },
                    ]
                },
                {
                    "mbbs": "mbbs002", #目标标识
                    "yxj": 1,   #优先级
                    "dxdl":[
                        {
                            "zzwqxhnm": "zzwqxhnm003", #需要weapon型号内码
                            "zdblxnm": "ZDBLXNM003",  #zdb类型
                            "dl": 2,    #数量
                        },
                        {
                            "zzwqxhnm": "zzwqxhnm004", #需要weapon型号内码
                            "zdblxnm": "ZDBLXNM004",  #zdb类型
                            "dl": 2,    #数量
                        },
                    ]
                }
            ]
        }
    ]
}

ssya = {  #预案明细
    "result": [
        {
            "rwbs": "task001",
            "ssyabs": "ssyabs001", #预案标识（对应上面两个表）
            "sslbs": "fscbs001-ssl0", #ssl标识(来自ssl_list)
            "sslmc": "fscnm001-ssl0", #ssl名称
            "mbbs": "mbbs001", #目标标识
            "zcptbs": "fscbs001", #ZC平台标识(来自ssl_list)
            "zckssj": "2024-04-29 17:55:03", #ZC开始时间(来自ssl_list)
            "zcjssj": "2024-04-29 17:55:03", #ZC结束时间(来自ssl_list)
            "zhptbs": "fscbs001", #ZH平台标识(来自ssl_list)
            "hlptbs": "fscbs001", #HL平台标识(来自ssl_list)
            "djkssj": "2024-04-29 17:55:03", #打击开始时间
            "djjssj": "2024-04-29 17:55:03", #打击结束时间
            "djbhsj": 100, #运行时间（来自ssl_list）
            "ydsl": 2, #用D数量
        },
        {
            "rwbs": "task001",
            "ssyabs": "ssyabs001", #预案标识（对应上面两个表）
            "sslbs": "fscbs001-ssl1", #ssl标识(对应杀伤链清单)
            "sslmc": "fscnm001-ssl0", #ssl名称(d)
            "mbbs": "mbbs001", #目标标识
            "zcptbs": "fscbs001", #ZC平台标识(来自ssl_list)
            "zckssj": "2024-04-29 17:55:03", #ZC开始时间(来自ssl_list)
            "zcjssj": "2024-04-29 17:55:03", #ZC结束时间(来自ssl_list)
            "zhptbs": "fscbs001", #ZH平台标识(来自ssl_list)
            "hlptbs": "fscbs001", #HL平台标识(来自ssl_list)
            "djkssj": "2024-04-29 17:55:03", #打击开始时间
            "djjssj": "2024-04-29 17:55:03", #打击结束时间
            "djbhsj": 120, #运行时间（来自ssl_list）
            "ydsl": 2, #用D数量
        }
    ]
}

hspj = { #毁伤判决，这个是提前注入的，格式可以你们自己定
    "zzwqxhnm":[ #型号内码
        {
            "zdblxnm": "ZDBLXNM001",  #zdb类型
            "mbbs": "mbbs001", #目标标识
            "1": 1,
            "2": 2,
            "3": 5,
            "4": 6,
            "5": 7
        },
        {
            "zdblxnm": "ZDBLXNM001",  #zdb类型
            "mbbs": "mbbs002", #目标标识
            "1": 1,
            "2": 2,
            "3": 5,
            "4": 6,
            "5": 7
        }
    ]
}

with open("weapons.json", "w") as f:
    json.dump(weapons, f)

with open("targets.json", "w") as f:
    json.dump(targets, f)

with open("ssl_list.json", "w") as f:
    json.dump(ssl_list, f)

with open("yapg.json", "w") as f:
    json.dump(yapg, f)

with open("dlgh.json", "w") as f:
    json.dump(dlgh, f)

with open("ssya.json", "w") as f:
    json.dump(ssya, f)

with open("hspj.json", "w") as f:
    json.dump(hspj, f)


