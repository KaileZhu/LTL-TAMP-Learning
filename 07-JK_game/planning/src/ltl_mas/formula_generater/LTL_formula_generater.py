import copy
import time

from planning.data.input_data.LTL_formula import *


class LTL_generater(object):
    def __init__(self,Data_manager):
        '''
        这是一套为了避免指战员使用困难，公式化生成形式化语言的方法。
        通过设定，波次，战法，内容进行自动化的生成形式化语言方法
        '''


        self.operation_atom = operation_atom
        self.tactics_atom = tactics_atom
        self.action_atom = action_atom
        self.formula_list = {}
        self.tactics_structure = tactics_structure
        self.operation_structure = operation_structure
        self.Data_manager = Data_manager
        self.specially_action_structure=specially_action_structure

    def creat_LTL_formula_with_wave_picking(self,to_replace_itom,action_atom ):
        self.formula_list_wave={}
        for round,current_itom in to_replace_itom.items():
            #current_rules=rules1[round]
            #获取当前波次下的数据
            ltl_formula=self.create_one_LTL_formula_with_default(current_itom,action_atom )
            self.formula_list_wave[round]=ltl_formula

    def create_one_LTL_formula_with_default(self,to_replace_itom,action_atom,rules1={}):
        '''
        战法中包涵几类战术，其中战术允许多次调用，
        to_replace_itom=[{'goal':'uav', 'place':'c'},{'place':'c'}]
        是战术类型中需要修改的部分，若没有则采用缺省的设置
        action_atom 即为要使用的战术类型
        rules 额外添加的条例
        通过条例+战术类型，能确定一个特殊的ltl公式，然后提供to_replace_itom 转换为带目标，的ltl公式。
        '''
        #生成基础的ltl公式
        #然后添加新的条例任务
        #task_and_rules_list=self.rules_solver(action_atom,rules,subtask_list)
        #生成基础的LTL公式
        #这一层是战术
        new_formula = A_formula()
        print('error?',to_replace_itom)
        new_formula.goal_subject_pair = to_replace_itom
        new_formula.action_type = action_atom
        print(operation_dic[action_atom])
        new_formula.action_list = basic_structure[operation_dic[action_atom]]
        self.generate_LTL_formula(new_formula)
        ltl_formula=new_formula.LTL_formula
        #根据rule,添加条例，使之成为完整的ltl公式
        rules1={}
        for rule_key, rule_item in rules1.items():
            num_z=0
            for rules in rule_item:
                for rule in rules:
                    if rule in basic_rule:
                        rule_formula = self.create_rule_formule(to_replace_itom[rule_key][num_z],rule)
                        ltl_formula[rule_key][num_z] = ltl_formula[rule_key][num_z] + ' && '+rule_formula
                    else:
                        raise  ValueError('未定义的条例')
                    num_z=num_z+1
        #self.formula_list.update(ltl_formula)
        return ltl_formula


    def pre_calculate_the_goal_data(self,value_place_dic,operation_type):
        #敌军的地区价值排序
        #自己的地区价值排序

        operation_type=operation_dic[operation_type]
        operation_structure=Place_structure[operation_type]
        final_struture=copy.copy(Pre_define_struture[operation_type])
        for waves,sub_operation in operation_structure.items():
            for key_words,goal_list in sub_operation.items():
                round=0
                for i in goal_list['place'][1]:
                    place=value_place_dic[goal_list['place'][0]][i]
                    print(final_struture)
                    final_struture[waves][key_words][0][round]['place']=place
                    round=round+1
        print('managed_final_structure',final_struture)
        #重新修改格式，方便界面识别
        #print(final_struture)
        final_struture2=[]
        # [{'number':'1','method':'基础侦查','target_sub':'红方','target_loc':'001','target_obj':'蓝方','target_sta':'动态'} for _ in range(5)]
        dic_zanshu={'basic_obs':'联合侦察',
                    'basic_atk':'联合进攻',
                    'order_obs':'梯度侦察',
                    'order_atk':'梯度进攻',
                    'order_support':'梯度支持',
                    'basic_support':'联合支持',
                    'basic_trick':'诱骗'}
        time.sleep(2)
        print('final_struture',final_struture)
        for waves, sub_operation in final_struture.items():
            for method, sub_list in sub_operation.items():
                print('sub_list',sub_list)
                for final_dic in sub_list[0]:
                    row={'number':waves+1,'method':dic_zanshu[method],'target_sub':'红方','target_loc':map_dic_to_num[final_dic['place']],
                         'target_obj':name_dic_to_blue[final_dic['goal']],'target_sta':'动态'}

                    #row1={'number':'1','method':'基础侦查','target_sub':'红方','target_loc':'001','target_obj':'蓝方','target_sta':'动态'}
                    final_struture2.append(row)
        #print(final_struture2)
        return final_struture2

    def pre_calculate_the_goal_data2(self,value_place_dic,operation_type):
        #敌军的地区价值排序
        #自己的地区价值排序

        operation_type=operation_dic[operation_type]
        operation_structure=Place_structure[operation_type]
        final_struture=copy.copy(Pre_define_struture[operation_type])
        for waves,sub_operation in operation_structure.items():
            for key_words,goal_list in sub_operation.items():
                round=0
                for i in goal_list['place'][1]:
                    place=value_place_dic[goal_list['place'][0]][i]
                    print(final_struture)
                    final_struture[waves][key_words][0][round]['place']=place
                    round=round+1
        print('managed_final_structure',final_struture)
        return final_struture

    def judge_the_goal(self,to_replace_itom,action_atom):
        z=0
        subtask_list={}
        for goal_tuple in to_replace_itom:
            place=goal_tuple['place']
            if 'goal' in goal_tuple.keys():
                goal=goal_tuple['goal']
            else:
                goal=dafualt_set[action_atom][z]
            count=self.check_if_has_agent(place, goal)
            #if count==0:
                #这个动作就不需要执行了
            subtask_list[z]=count
            z=z+1
        return  subtask_list

    def check_if_has_agent(self,place,goal):
        count=0
        for agent_name in self.Data_manager.map_2_agent[place]:
            if goal=='all':
                count=count+1
            if goal in agent_name:
                count=count+1
        return count

    def create_one_LTL_formula2(self, goal_subject_pair, action_type):
        '''
		goal_subject_pair=[(gaol,subject)]
		:param goal_subject_pair:
		:param action_type:
		:return:
		'''
        new_formula = A_formula()
        new_formula.goal_subject_pair = goal_subject_pair
        new_formula.action_type = action_type
        new_formula.action_list = operation_structure[action_type]
        self.generate_LTL_formula(new_formula)
        self.formula_list.append(new_formula)

    def user_defined_one_LTL_formula(self, goal, subject):
        new_formula = A_formula()
        new_formula.goal = goal
        new_formula.subject = subject
        new_formula.action_type = 'User_defined'
        self.formula_list.append(new_formula)

    def check_current_LTL_formula(self):
        i = 1
        for subformula in self.formula_list:
            print('formula', i, ': ', subformula)
            i = i + 1

    def create_rule_formule(self,to_replace_itom,rule):
        # 判断rule是否激活，若没有激活则返回空
        if self.judge_the_rules(to_replace_itom,rule):
            return ''
        LTL_rule=rule_structure[rule]['LTL']
        first_=0
        second_=0
        rount_count=0
        final_ltl_list=''
        for word in LTL_rule:
            if word=='_':
                if first_==0:
                    first_=1
                    start_count=rount_count
                else:
                    second_=1
                    end_count=rount_count
                if second_==1:
                    first_=0
                    second_=0
                    number=LTL_rule[start_count+1:end_count]
                    place=to_replace_itom[int(number)]['place']
                    created_word=rule_structure[rule][number]['subject']+'_' + \
                                 rule_structure[rule][number]['act']+'_' + \
                                 place+'_'+rule_structure[rule][number]['goal']
                    final_ltl_list=final_ltl_list+created_word

            else:
                if not first_==1:
                    final_ltl_list=final_ltl_list+word
            rount_count=rount_count+1
        return final_ltl_list

    def generate_LTL_formula(self, new_formula):
        ltl_formula = {}
        i = 0
        goal_subject_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        number_z = 0
        #print(new_formula.action_list)
        #print(new_formula.goal_subject_pair)
        for war_action in new_formula.action_list:
            if not war_action in new_formula.goal_subject_pair.keys():
                continue
            number_z=0
            goal_subject_dic = {}
            for goal_tuple in new_formula.goal_subject_pair[war_action]:
                number_z=0
                print('goal_tuple',goal_tuple)
                for goal in goal_tuple:
                    goal_subject_dic[goal_subject_list[number_z]] = goal
                    number_z = number_z + 1
                print('goal_subject_dic',goal_subject_dic)
                sub_formula = self.action_generate(goal_subject_dic, war_action)
                if not war_action in ltl_formula.keys():
                    ltl_formula[war_action]=[]
                    ltl_formula[war_action].append(sub_formula)
                else:
                    ltl_formula[war_action].append(sub_formula)
        new_formula.LTL_formula = ltl_formula

    def judge_the_rules(self,to_replace_itom,rule):
        if 'condition' in rule_structure[rule].keys():
            place =to_replace_itom[0]['place']
            for required_type, required_list in rule_structure[rule]['condition'].items():
                if required_type=='with':
                    goal_count=0
                    for goal in required_list:
                        if goal in self.Data_manager.map_with_agent[place]:
                            goal_count=goal_count+1
                    if goal_count == 0:
                        return  0
                if required_type == 'without':
                    for goal in required_list:
                        if goal in self.Data_manager.map_2_agent[place]:

                            return  0
            return 1
        else:
            return  0


    def action_generate(self, goal_subject_dic, action):
        if action not in self.specially_action_structure:
            if not action == 'User_defined':
                raise ValueError('Use undefined ltl symbols')
        '''有一些特别的action，得现场构建时序约束'''
        if action in self.specially_action_structure:
            print(action)
            action_table=self.get_special_action_table(goal_subject_dic,action)
        else:
            action_table = self.tactics_structure[action]
        first_ = 0
        second_ = 0
        start = 0
        third_ = 0
        count = 0
        new_action_table = ''
        for str_1 in action_table:
            '''
			this step is to find out the  _1_ label and change it into the subjuect_1_goal '''
            basic_word_founded = 0
            if str_1 == '_':
                # start 0 not found _  1 found first _  2 found second _
                if first_ == 0:
                    first_ = 1
                    count_start = count
                    start = 1
                    basic_word_founded = 1
                elif second_ == 0:
                    second_ = 1
                    count_mid = count
                    basic_word_founded = 1
                elif third_ == 0:
                    third_ = 1
                    count_end = count
                    basic_word_founded = 1
                    start = 0
            if not third_:
                if not start:
                    new_action_table = new_action_table + str_1
            else:
                word_key = action_table[count_start + 1:count_mid]
                action_key = action_table[count_mid + 1:count_end]
                # print(word_key)
                if 'subject' in goal_subject_dic[action_key].keys():
                    subject=goal_subject_dic[action_key]['subject']
                else:
                    subject=default_tactics_dic[action][action_key]['subject']
                if 'place' in goal_subject_dic[action_key].keys():
                    area=goal_subject_dic[action_key]['place']
                else:
                    area=default_tactics_dic[action][action_key]['subject']
                if 'goal' in goal_subject_dic[action_key].keys():
                    goal = goal_subject_dic[action_key]['goal']
                else:
                    goal=default_tactics_dic[action][action_key]['subject']
                #subject, area, goal = goal_subject_dic[action_key]['subject'],goal_subject_dic[action_key]['place'],goal_subject_dic[action_key]['goal']
                symbols = self.symbol_creater(subject, area, goal, word_key)
                new_action_table = new_action_table + symbols
                first_ = 0
                second_ = 0
                third_ = 0
            count = count + 1
        print(goal_subject_dic)
        return new_action_table


    def get_special_action_table(self,goal_subject_dic,action):
        #{'order_atk', 'order_obs', 'basic_obs', 'basic_atk', 'basic_support'}
        if action == 'order_obs':
            n=len(goal_subject_dic)
            #create a sequence
            action_symbol='1'
            round=0
            ltl_formula=''
            round_dic=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s']
            for i in range(n):
                if round==0:
                    ltl_formula=ltl_formula+'<> ( _'+action_symbol+'_'+round_dic[round]+'_ '
                else:
                    ltl_formula = ltl_formula + '&& <> ( _' + action_symbol + '_' + round_dic[round] + '_'
                round=round+1
            ltl_formula=ltl_formula+')'*n
            for i in range(n-1):
                ltl_formula=ltl_formula+'&& [] ( _'+action_symbol+'_'+round_dic[i]+'_ -> ! _'+action_symbol+'_'+round_dic[i+1]+'_)'
            return  ltl_formula
        elif action == 'order_atk':
            n = len(goal_subject_dic)
            # create a sequence
            action_symbol = '0'
            round = 0
            ltl_formula = ''
            round_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            for i in range(n):
                if round == 0:
                    ltl_formula = ltl_formula + '<> ( _' + action_symbol + '_' + round_dic[round] + '_ '
                else:
                    ltl_formula = ltl_formula + ' && <> ( _' + action_symbol + '_' + round_dic[round] + '_'
                round = round + 1
            ltl_formula = ltl_formula + ')' * n
            for i in range(n - 1):
                ltl_formula = ltl_formula + '&& [] ( _' + action_symbol + '_' + round_dic[
                    i] + '_ -> ! _' + action_symbol + '_' + round_dic[i + 1] + '_) '
            return ltl_formula
        elif action == 'basic_obs':
            n = len(goal_subject_dic)
            # create a sequence
            action_symbol = '1'
            round = 0
            ltl_formula = ''
            round_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            for i in range(n):
                if round==0:
                    ltl_formula = ltl_formula + '<>  _' + action_symbol + '_' + round_dic[round] + '_ '
                else:
                    ltl_formula = ltl_formula + '&& <>  _' + action_symbol + '_' + round_dic[round] + '_ '
                round = round + 1
            return ltl_formula
        elif action == 'basic_atk':
            n = len(goal_subject_dic)
            # create a sequence
            action_symbol = '0'
            round = 0
            ltl_formula = ''
            round_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            for i in range(n):
                if round == 0:
                    ltl_formula = ltl_formula + '<>  _' + action_symbol + '_' + round_dic[round] + '_ '
                else:
                    ltl_formula = ltl_formula + '&& <>  _' + action_symbol + '_' + round_dic[round] + '_ '
                round = round + 1
            return ltl_formula
        elif action == 'basic_support':
            n = len(goal_subject_dic)
            # create a sequence
            action_symbol = '3'
            round = 0
            ltl_formula = ''
            round_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            for i in range(n):
                if round == 0:
                    ltl_formula = ltl_formula + '<>  _' + action_symbol + '_' + round_dic[round] + '_ '
                else:
                    ltl_formula = ltl_formula + '&& <>  _' + action_symbol + '_' + round_dic[round] + '_ '
                round = round + 1
            return ltl_formula
        elif action == 'order_support':
            n = len(goal_subject_dic)
            # create a sequence
            action_symbol = '3'
            round = 0
            ltl_formula = ''
            round_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            for i in range(n):
                if round == 0:
                    ltl_formula = ltl_formula + '<> ( _' + action_symbol + '_' + round_dic[round] + '_ '
                else:
                    ltl_formula = ltl_formula + ' && <> ( _' + action_symbol + '_' + round_dic[round] + '_'
                round = round + 1
            ltl_formula = ltl_formula + ')' * n
            for i in range(n - 1):
                ltl_formula = ltl_formula + '&& [] ( _' + action_symbol + '_' + round_dic[
                    i] + '_ -> ! _' + action_symbol + '_' + round_dic[i + 1] + '_) '
            return ltl_formula
        elif action == 'basic_trick':
            n = len(goal_subject_dic)
            # create a sequence
            action_symbol = '4'
            round = 0
            ltl_formula = ''
            round_dic = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
            for i in range(n):
                if round == 0:
                    ltl_formula = ltl_formula + '<>  _' + action_symbol + '_' + round_dic[round] + '_ '
                else:
                    ltl_formula = ltl_formula + '&& <>  _' + action_symbol + '_' + round_dic[round] + '_ '
                round = round + 1
            return ltl_formula
        raise  ValueError('Not defined action')

    def create_final_formula(self):
        #在这里考虑进去波次
        self.final_formula = {}
        i = 1
        for round,formula_list in self.formula_list_wave.items():
            self.final_formula[round]=[]
            for furmula_name, formula_list in formula_list.items():
                self.final_formula[round].extend(formula_list)
            i=i+1
        #for furmula_name, formula_list in self.formula_list.items():
        #    for sub_formula in formula_list:
        #        if len(self.final_formula) < i:
        #            self.final_formula.append('')
        #        if not len(self.final_formula[i - 1]) == 0:
        #            self.final_formula[i - 1] = self.final_formula[i - 1] + ' && ' + sub_formula
        #        else:
        #            self.final_formula[i - 1] = self.final_formula[i - 1] + sub_formula
        #        block_count = 0
        #        for sign in self.final_formula[i - 1]:
        #            if sign == ' ':
        #                block_count = block_count + 1
        #        if block_count > 20:
        #            i = i + 1
        print('final formula is ', self.final_formula)

    def symbol_creater(self, subject, area, goal, word_key):
        word = self.action_atom[word_key]
        # if self.word_tyoe[word]=='':
        # new_word='_'+subject+'_'+word+'_'+goal+'_'
        new_word = subject + '_' + word + '_' + area + '_' + goal
        return new_word


class A_formula(object):
    def __init__(self):
        # subject is the one who execute the action
        self.subject = None
        # goal
        self.goal = None
        # action_type: Follow_defend, user-defined,
        self.action_type = None
        self.LTL_formula = None
        self.action_list = None
        self.goal_subject_pair = None

    def detail(self):
        return self.goal_subject_pair, self.action_type, self.LTL_formula
