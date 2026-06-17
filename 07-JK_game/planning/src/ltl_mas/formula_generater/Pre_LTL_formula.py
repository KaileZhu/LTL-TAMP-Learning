from  data.input_data.LTL_formula import *


class LTL_generater(object):
	def __init__(self):
		self.operation_atom=operation_atom
		self.tactics_atom=tactics_atom
		self.action_atom=action_atom
		self.formula_list=[]
		self.tactics_structure=tactics_structure


	def create_one_LTL_formula(self,goal_subject_pair,action_type):
		'''
		goal_subject_pair=[(gaol,subject)]
		:param goal_subject_pair:
		:param action_type:
		:return:
		'''
		new_formula=A_formula()
		new_formula.goal_subject_pair=goal_subject_pair
		new_formula.action_type=action_type
		new_formula.action_list=operation_structure[action_type]
		self.generate_LTL_formula(new_formula)
		self.formula_list.append(new_formula)

	def create_one_LTL_formula2(self,goal_subject_pair,action_type):
		'''
		goal_subject_pair=[(gaol,subject)]
		:param goal_subject_pair:
		:param action_type:
		:return:
		'''
		new_formula=A_formula()
		new_formula.goal_subject_pair=goal_subject_pair
		new_formula.action_type=action_type
		new_formula.action_list=operation_structure[action_type]
		self.generate_LTL_formula2(new_formula)
		self.formula_list.append(new_formula)

	def user_defined_one_LTL_formula(self,goal,subject):
		new_formula=A_formula()
		new_formula.goal=goal
		new_formula.subject=subject
		new_formula.action_type='User_defined'
		self.formula_list.append(new_formula)

	def check_current_LTL_formula(self):
		i=1
		for subformula in self.formula_list:
			print('formula',i,': ',subformula.detail())
			i=i+1


	def generate_LTL_formula(self,new_formula):
		ltl_formula=''
		i=0
		for subject,area ,goal in new_formula.goal_subject_pair:
			action=new_formula.action_list[i]
			sub_formula=self.action_generate(subject,action,area,goal)
			if len(ltl_formula)>0:
				ltl_formula=ltl_formula+' && '+sub_formula
			else:
				ltl_formula=sub_formula
			i=i+1
		new_formula.LTL_formula=ltl_formula
		print(new_formula.LTL_formula)
		print(ltl_formula)

	def generate_LTL_formula2(self,new_formula):
		ltl_formula=''
		i=0
		goal_subject_list=['a','b','c','d','e','f','g','h']
		goal_subject_dic={}
		number_z=0
		for goal in new_formula.goal_subject_pair:
			goal_subject_dic[goal_subject_list[number_z]]=goal
			number_z=number_z+1
		for action in new_formula.action_list:
			sub_formula=self.action_generate2(goal_subject_dic,action)
			if len(ltl_formula)>0:
				ltl_formula=ltl_formula+' && '+sub_formula
			else:
				ltl_formula=sub_formula
			i=i+1
		new_formula.LTL_formula=ltl_formula
		print(new_formula.LTL_formula)
		print(ltl_formula)

	def action_generate(self,subject,action,area, goal):
		if action not in tactics_atom:
			if not  action=='User_defined':
				raise ValueError('Use undefined ltl symbols')
		action_table=self.tactics_structure[action]
		start=0
		end=0
		count=0
		new_action_table=''
		for str_1 in action_table:
			'''
			this step is to find out the  _1_ label and change it into the subjuect_1_goal '''
			basic_word_founded=0
			if str_1=='_':
				basic_word_founded=0
				#start 0 not found _  1 found first _  2 found second _
				if start==1:
					count_end=count
					start=0
					basic_word_founded=1
				elif start==0:
					count_begin=count
					start=1
			if not basic_word_founded:
				if not start:
					new_action_table=new_action_table+str_1
			else:
				word_key=action_table[count_begin+1:count_end]
				#print(word_key)
				symbols=self.symbol_creater(subject,area,goal,word_key)
				new_action_table=new_action_table+symbols
			count=count+1
		return new_action_table

	def action_generate2(self,goal_subject_dic,action):
		if action not in tactics_atom:
			if not  action=='User_defined':
				raise ValueError('Use undefined ltl symbols')
		action_table=self.tactics_structure[action]
		first_=0
		second_=0
		start=0
		third_=0
		count=0
		new_action_table=''
		for str_1 in action_table:
			'''
			this step is to find out the  _1_ label and change it into the subjuect_1_goal '''
			basic_word_founded=0
			if str_1=='_':
				#start 0 not found _  1 found first _  2 found second _
				if first_==0:
					first_=1
					count_start=count
					start=1
					basic_word_founded=1
				elif second_==0:
					second_=1
					count_mid=count
					basic_word_founded = 1
				elif third_==0:
					third_=1
					count_end=count
					basic_word_founded=1
					start=0
			if not third_:
				if not start:
					new_action_table=new_action_table+str_1
			else:
				word_key=action_table[count_start+1:count_mid]
				action_key=action_table[count_mid+1:count_end]
				#print(word_key)
				subject,area,goal=goal_subject_dic[action_key]
				symbols=self.symbol_creater(subject,area,goal,word_key)
				new_action_table=new_action_table+symbols
				first_=0
				second_=0
				third_=0
			count=count+1
		return new_action_table
	def create_final_formula(self):
		self.final_formula=[]
		i=1
		for sub_formula in self.formula_list:
			if len(self.final_formula)<i:
				self.final_formula.append('')
			if not len(self.final_formula[i-1])==0:
				self.final_formula[i-1]=self.final_formula[i-1]+' && '+sub_formula.LTL_formula
			else:
				self.final_formula[i-1]=self.final_formula[i-1]+sub_formula.LTL_formula
			block_count=0
			for sign in self.final_formula[i-1]:
				if sign == ' ':
					block_count=block_count+1

			if block_count>20:
				i=i+1
		print('final formula is ',self.final_formula)

	def symbol_creater(self,subject,area,goal,word_key):
		word=self.action_atom[word_key]
		#if self.word_tyoe[word]=='':
		#new_word='_'+subject+'_'+word+'_'+goal+'_'
		new_word=subject+'_'+word+'_'+area+'_'+goal
		return new_word


class A_formula(object):
	def __init__(self):
		# subject is the one who execute the action
		self.subject=None
		# goal
		self.goal=None
		# action_type: Follow_defend, user-defined,
		self.action_type=None
		self.LTL_formula=None
		self.action_list=None
		self.goal_subject_pair=None

	def detail(self):
		return self.goal_subject_pair,self.action_type,self.LTL_formula
