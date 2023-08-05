# encoding: utf-8
"""
@author: liuwz
@time: 2021/6/16 10:53 上午
@file: main.py
@desc: 
"""
import sys
from typing import List
import os
from plumbum import cli, colors


class TcrCli(cli.Application):
    cmd_dict = {}
    cmd_help = {}
    with cli.Config(f'{os.path.abspath(__file__)}/../conf/cmd.conf') as cmdConf:
        for key, option in cmdConf.parser.items("DEFAULT"):
            optionArr = option.split(";")
            cmd_help[key] = optionArr[0]
            cmd_dict[key] = optionArr[1]

    @cli.switch(
        ["-h", "--help"],
        overridable=True,
        group="Meta-switches",
        help=("""Prints this help message and quits"""),
    )

    def help(self):
        #super().help()
        print("TCR-CLI" + "\t" + "1.0"
                                 "\n" | colors.green)
        print("USAGE:\n  tcrcli <command> [options]\n")
        print("Commands:")
        for k, v in self.cmd_help.items():
            print("  " + format(k, "<25"), format(v, "<25"))
        print('\t')
        print("示例：tcrcli ls /")

    def main(self, *args):
        # 初始化配置
        with cli.Config(f'{os.path.abspath(__file__)}/../conf/tcr.conf') as conf:
            _confSection = conf['confSection']
            _ip = conf["%s.ip" % _confSection]
            _port = conf["%s.port" % _confSection]

        # 执行系统命令
        def executeSystemCmd(cmd):
            os.system(cmd)


        if args.__len__() == 3:
            if args[0] == "setlevel":
                _module = args[1]
                _level = args[2]
                if _level not in ["debug", "info", "warning", "error"]:
                    print('输入日志等级有误，请重新输出!' | colors.red)
                    return
                cmd = f'curl -X POST "http://{_ip}:{_port}/v2/temps/loglevel/{_module}/{_level}" -H "accept: ' \
                      f'application/json"'
                executeSystemCmd(cmd)
        elif args.__len__() == 2:
            if args[0] == "ls":
                _dir = args[1]
                cmd = f"ls -a {_dir}"
                executeSystemCmd(cmd)


if __name__ == '__main__':
    TcrCli.run()