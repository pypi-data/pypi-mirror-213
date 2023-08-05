# GPL License
# Copyright (C) UESTC
# All Rights Reserved 
#
# @Time    : 2022/4/25 0:17
# @Author  : Xiao Wu
# @reference:

def run_demo():

    from pancollection import TaskDispatcher, trainer, build_model, getDataSession
    cfg = TaskDispatcher.new(task='pansharpening', mode='entrypoint', arch='FusionNet')
    print(TaskDispatcher._task.keys())
    trainer.main(cfg, build_model, getDataSession)
    # or
    # import pancollection as pan
    # cfg = pan.TaskDispatcher.new(task='pansharpening', mode='entrypoint', arch='FusionNet')
    # print(pan.TaskDispatcher._task)
    # pan.trainer.main(cfg, pan.build_model, pan.getDataSession)

if __name__ == '__main__':
    run_demo()