# JK_game
一个博弈算法
具体处理思路
1 选取合适的场景
2 选取战法
3 根据战法生成LTL公式
4 根据LTL公式生成偏序
5 基于偏序生成的分配内容

开启步骤 前端
1 运行jk_game/CentralServer__master文件（后端）
2 运行jk_game/planning/src/gui/main.py文件（前端）
3 点击central_master文件跳出的网址 则打开访问界面

然后依次完成 场景选择  算法选择，偏好选择，战法选择，点击生成战法内容 
  战术编辑，点击生成子任务

以上任何一步出问题，请从打开文件开始

#----------------------------------------------
以下是对每一个模块负责的部分的解释
整体的控制程序在planning/src/central_master.py 的central_master中
之下分为Data_pretreat LTL_generater Data_pretreat Poset_producter fuzzy_topsis_method 五个模块
Data_manager 负责统筹数据信息，一般要查询的数据信息都在这里面

LTL_generater 负责将输入的算法格式生成LTL公式
        在central_master中的136行
        self.task = LTL_generater(self.Data_manager)
        #self.rules = software_input_data['rule']
        处理输入的问题

        self.task.creat_LTL_formula_with_wave_picking(new_input, method_name)
Poset_producter 负责将输入的LTL公式转换为偏序poset
        #self.Poset_product.generate_poset() #生成偏序
        #self.Poset_product.prodocter()
        #self.poset=self.Poset_product.final_poset #最终获得的偏序
        # 根据环境，评估子任务的内容，以及价值
        #self.Data_manager.estimate_cost_of_tasks(self.Poset_product) #估算代价
        #self.input_data = self.Data_manager.input_data 
fuzzy_topsis_method 负责模糊决策 
之后的功能删改请遵循以上原则，让相关的功能放到一个模块内。


  
