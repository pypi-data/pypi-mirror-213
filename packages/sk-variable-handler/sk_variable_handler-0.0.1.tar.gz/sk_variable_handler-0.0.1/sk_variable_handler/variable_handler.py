import regex

class VariableHandler:


    def __init__(self):

        self.constant_expression_list ={}
        self.variable_expression_list=[]
        self.declaration_list = {}
        self.comment_list = {}

    def set_calculator(self,calculator):
        self.calculator = calculator

    def declare(self,declarations):

        declarations = self.remove_comments(declarations)

        declarations = list(filter(None, regex.split(r'[;,]',declarations)))

        for declaration in declarations:
            declaration = list(filter(None, regex.split(r'\s*(\$[^=]+)=',declaration)))
            variable =declaration[0].replace(' ','')
            expression =declaration[1]
            self.declaration_list[variable] = expression


    def get_constant_expression_list (self):


        for variable,expressin in self.declaration_list.items():
            if '$' not in expressin:
                self.constant_expression_list[variable] = str(self.calculator.evaluate(expressin))

        for variable,expressin in self.constant_expression_list.items():
            self.declaration_list[variable] = expressin

    def get_variable_expression_list(self):


        for variable,expressin in self.declaration_list.items():
            if '$' in expressin:
                self.variable_expression_list.append((variable,expressin))

    def solve_variable_expression_list(self):
        temp = {}
        for variable,expressin in self.variable_expression_list:
            temp_expression =expressin
            for key,value in self.constant_expression_list.items():
                pattern = regex.escape(key)+r'(\s|\b)'
                temp_expression = regex.sub(pattern,str(value),temp_expression)
            temp[variable] =temp_expression

        for variable,expression in temp.items():
            if '$' not in expression:
                self.constant_expression_list[variable]=str(self.calculator.evaluate(expression))
                for variable_e in self.variable_expression_list:
                    if variable_e[0] == variable:
                       self.variable_expression_list.remove(variable_e)

                self.declaration_list[variable]=str(self.calculator.evaluate(expression))
            else:
                self.variable_expression_list.append((variable,expression))
                self.declaration_list[variable]=expression

        for key,value in  self.variable_expression_list:
            if '$' in value:
                self.solve_variable_expression_list()

    def remove_comments(self,declaration):
        pattern = r'(#[^\$]+)'

        return regex.sub(pattern,'',declaration)

    def get_values(self,declarations):
        self.declare(declarations)
        self.get_constant_expression_list()
        self.get_variable_expression_list()
        self.solve_variable_expression_list()

        return  self.declaration_list

