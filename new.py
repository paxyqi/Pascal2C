error_num = 0

import ply.lex as lex  # 导入python lex模块

tokens = [
    # 算术运算符
    # 'DIV', 'MOD',
    # 关系运算符
    'NOTGREATER', 'NOTLESS', 'NOTEQUAL',
    # 逻辑运算符
    # 'NOT', 'AND', 'OR',
    # 赋值运算符
    'ASSIGN',
    # 界符
    'ANNOTATION', 'AREA',
    # 常量
    'NUMINT', 'NUMFLOAT', 'LETTER',
    'IL_ID','IL_LETTER',
    # 标识符
    'ID',
    # 换行符
    'LF',
    'TAB',

]

literals = ['=', '-', '*', '/', '(', ')', ';', '<', '>', ',', '[', ']', ':', '+', '.']

# 关键字/保留字；本质上也可以写在tokens，但这里单独处理效率高
reserved = {
    'var': 'VAR',
    'integer': 'INTEGER',
    'real': 'REAL',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'function': 'FUNCTION',
    'div' : 'DIV',
    'mod' : 'MOD',
    'not' : 'NOT',
    'and' : 'AND',
    'or' : 'OR',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'begin': 'BEGIN',
    'end': 'END',
    'array': 'ARRAY',
    'case': 'CASE',
    'of': 'OF',
    'class': 'CLASS',
    'const': 'CONST',
    'default': 'DEFAULT',
    'do': 'DO',
    'to': 'TO',
    'downto': 'DOWNTO',
    'finally': 'FINALLY',
    'goto': 'GOTO',
    'for': 'FOR',
    'procedure': 'PROCEDURE',
    'program': 'PROGRAM',
    'read': 'READ',
    'write': 'WRITE'
}

# 将保留字添加到tokens，因为lex只识别关键字tokens
tokens += reserved.values()

# 运算符
t_NOTEQUAL = r'<>'
t_NOTLESS = r'>='
t_NOTGREATER = r'<='


t_ASSIGN = r':='

# 界符
t_AREA = r'\.\.'

# 忽略空格
t_ignore = r' '


# 忽略注释
def t_ANNOTATION(t):
    r'(\{(.|\n)*?\})'  # 第一行写正则表达式
    t.lexer.lineno += t.value.count('\n')  # 累计行数
    pass  # 表示忽略该token


# 忽略换行
def t_LF(t):
    r'[ ]+\n'
    pass


# 忽略tab
def t_TAB(t):
    r'\t'
    pass

# ID错误情况
def t_IL_ID(t):
    r'[0-9]+[a-zA-Z][0-9a-zA-Z]*'
    print(f"========Illegal ID: {t.value}   line: {str(t.lineno)}========")

# char常量错误情况
def t_IL_LETTER(t):
    r'\'[^\']{2}'
    print(f"========Illegal letter: {t.value}   line: {str(t.lineno)}========")

# 识别数字
def t_NUMFLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)  # 返回是字符串类型，需转为float型
    return t


def t_NUMINT(t):
    r'[0-9]+'
    t.value = int(t.value)  # 返回是字符串类型，需转为整型
    return t


# 识别字符
def t_LETTER(t):
    r'\'[a-zA-Z]\''
    return t

# # 识别字符串
# def t_STRING(t):
#     r'(\'(.)*?\')'
#     return t


# 识别标识符
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if (len(t.value) > 63):  # 标识符长度限制
        t_error(t)
        pass
    else:
        t.value = t.value.lower()
        t.type = reserved.get(t.value, 'ID')
        return t


# 增加行数
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # 计算行数


# 错误处理：输出错误符号，行数，列数后跳过当前错误继续扫描
def t_error(t):
    tmp = t.lexpos - data.rfind('\n', 0, t.lexpos)
    print(f"========Illegal character: {t.value}   line: {str(t.lineno)}   col: {str(tmp)}========")
    t.lexer.skip(1)  # 跳过当前字符

# 调用Lex模块，构建词法分析器
lexer = lex.lex()
# ===================================================================================================
# 词法测试部分
# ===================================================================================================
# 测试输入文件与结果输出文件
# f1 = open('C:/Users/26925/Desktop/out.txt', 'w')   #输出结果
# f = open('test3.pas', 'r', encoding='UTF-8')
#
#
# data = f.read() # 获取输入串
#
# lexer.input(data) # 将输入串输入词法分析器
#
# # =============================================================================
# # 测试部分：真正运行时将其注释掉 / 将ISTEST设为False
# # =============================================================================
# ISTEST = True # 打开测试
# # ISTEST = False # 关闭测试
# if ISTEST:
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break  # No more input
#         print(tok)
#         tok = str(tok)
#         f1.write(tok)
#         f1.write("\n")
#
# # =============================================================================
# #  获取Token的接口
# # =============================================================================
# def getToken():
#     return lexer.token()
#
# # 文件流关闭
# f.close()
# f1.close()

# =====================================================================================================
# 语法分析部分
# =====================================================================================================
#
#


def p_error(p):
    global error_num
    error_num+=1
    if p:
        print("Syntax error at '%s'" %p.value," line:%d"%p.lexer.lineno)

    else:
        print("Syntax error at EOF")


# 符号表项
class ValueItem():
    def __init__(self,id_type,value_type,array,declare_row):
        self.id_type = id_type
        self.value_type = value_type
        self.array = array
        self.declare_row = declare_row
        self.used_row = []
    def use(self,line_num):
        self.used_row.append(line_num)
    def output(self):
        print(self.id_type,self.value_type,self.array,self.declare_row,self.used_row,sep=',')


# 插入符号表，检查重复定义,返回是否成功插入
def insert_value_table(id, valueItem):
    global error_num
    global global_value
    global local_value
    if (is_global):
        if (id in global_value.keys()):
            print("===ERROR===\nprevious definition of", id, "was here.", "line:", valueItem.declare_row, sep=' ')
            error_num += 1
            return 0
        else:
            global_value[id] = valueItem
            return 1
    else:
        if (id in local_value.keys()):
            print("===ERROR===previous definition of", id, "was here.", "line:", valueItem.declare_row, sep=' ')
            error_num += 1
            return 0
        else:
            local_value[id] = valueItem
            return 0


def p_program_1(p):
    '''programstruct : program_head ';' program_body '.' '''


def p_program_head_1(p):
    '''program_head : PROGRAM ID '('  idlist ')' '''

def p_program_head_2(p):
    '''program_head : PROGRAM ID'''


def p_program_body_1(p):
    '''program_body :   const_declarations var_declarations global_convert subprogram_declarations help_print_main compound_statement'''
    # print('}')

def p_global_convert(p):
    '''global_convert : '''
    global is_global
    is_global = 0

def p_help_print_main(p):
    '''help_print_main : '''
    print('int main()')
    # print('{')

def p_const_declarations_1(p):
    '''const_declarations :  CONST const_declaration ';' '''


def p_const_declarations_2(p):
    '''const_declarations :  '''


def p_const_declaration_1(p):#此处 c语言翻译应是const a=10，b=20； pascal是const a=10；b=20；中间的标点有不同，需要注意
    '''const_declaration :   const_declaration   ';' ID '='   const_value'''
    symbol = ValueItem('const', p[5][0],None, p.lineno(3))
    if(insert_value_table(p[3],symbol)):
        print('const', p[5][0], p[3], '=', p[5][1] + ';', sep=' ')


def p_const_declaration_2(p):
    '''const_declaration :   ID '=' const_value'''
    symbol = ValueItem('const', p[3][0], None, p.lineno(1))
    if(insert_value_table(p[1],symbol)):
        print('const', p[3][0], p[1], '=', p[3][1] + ';', sep=' ')

def p_const_value_1(p):
    '''const_value : '+' NUMINT
                    | '-' NUMINT'''
    p[0] = []
    p[0].append('int')
    p[0].append(p[1] + str(p[2]))

def p_const_value_2(p):
    '''const_value : '+' NUMFLOAT
                   | '-' NUMFLOAT'''
    p[0] = []
    p[0].append('double')
    p[0].append(p[1] + str(p[2]))

def p_const_value_3(p):
    '''const_value :  LETTER'''
    p[0] = []
    p[0].append('char')
    p[0].append(p[1])

def p_const_value_4(p):
    '''const_value :  NUMFLOAT'''
    p[0] = []
    p[0].append('double')
    p[0].append(str(p[1]))

def p_const_value_5(p):
    '''const_value :  NUMINT'''
    p[0] = []
    p[0].append('int')
    p[0].append(str(p[1]))

# def p_const_value_4(p):
#     '''const_value : '\'' LETTER '\'' '''
#     p[0]='\'' + (p[1]) + '\''
#=====================================================================attention!此处letter的处理暂时省略，之后讨论

# var_declarations ->var  var_declaration ;
# 		| empty
# var_declaration->var_declaration ; idlist :  type
# 		|   idlist :  type
# type->basic_type
# 	|  array [ period  ] of basic_type
# basic_type->integer
# 	| real
# 	|  boolean
# 	|  char
# period->period ， digits .. digits
# 	| digits .. digits
#
# subprogram_declarations->subprogram_declarations subprogram ;  |  empty
# subprogram->subprogram_head ;  subprogram_body
# subprogram_head->procedure id formal_parameter
# 		|   function  id formal_parameter :  basic_type
# formal_parameter->( parameter_list ) | empty
# parameter_list->parameter_list ;  parameter |  parameter





# ========================================================================
# 数组类，包括：
# dimension 数组维度，整型
# period 数组下标范围，字典型
# basictype 基本类型,str型
# ========================================================================
class Array():
    def __init__(self, period, basictype):
        self.name = 'array'
        self.baseType = basictype
        self.period = period
        self.dimension = len(period)


class Period():
    def __init__(self, level, low_bound, up_bound, period):
        self.level = level
        self.period = period
        bound = [low_bound, up_bound]
        self.period[self.level] = bound


# ==========================================================================
# 符号表，每个过程/函数的属性：
# 符号表 字典 key是变量名 value是[类型,array（数组用，做越界检查否则置为空）]
# ==========================================================================


# ==========================================================================
# 产生式列表
# ==========================================================================


# var_declarations ->var  var_declaration ;
# 		| empty
def p_var_declaration_list_1(p):
    '''var_declarations : VAR var_declaration ';' '''


def p_var_declaration_list_empty(p):
    '''var_declarations : '''


# var_declaration->var_declaration ; idlist :  type
# 		|   idlist :  type
def p_var_declaration_1(p):
    '''var_declaration : var_declaration ';' idlist ':' type'''
    # print(p[5] + ' ' + p[3] + ';')

    global error_num
    if isinstance(p[5],Array):
        # 检查维度
        flag = 1
        for i in range(0, p[5].dimension):
            bound = p[5].period[i + 1]
            if bound[0]>bound[1]:
                print('===ERROR===\n','ARRAY \'s upper bound is greater than lower bound! ','line: ',p.lineno(4))
                error_num+=1
                flag = 0
        if(flag):
            symbol = ValueItem('var', 'Array', p[5], p.lineno(4))
            for x in p[3]:
                if(insert_value_table(x,symbol)):
                    print(p[5].baseType + ' ' + x, end='')
                    for i in range(0, p[5].dimension):
                        bound = p[5].period[i + 1]
                        print('[' + str(bound[1] - bound[0] + 1) + ']', end='')
                    print(';')
    else:
        symbol = ValueItem('var', p[5], None, p.lineno(4))
        for x in range(0,len(p[3])):
            if(insert_value_table(x, symbol)):
                print(p[5] + ' ' + p[3][x] + ';')
        print(';')


def p_var_declaration_2(p):
    '''var_declaration : idlist ':' type'''
    global error_num
    if isinstance(p[3],Array):
        # 检查维度
        flag = 1
        for i in range(0, p[3].dimension):
            bound = p[3].period[i + 1]
            if bound[0]>bound[1]:
                print('===ERROR===\n','ARRAY \'s upper bound is greater than lower bound! ','line: ',p.lineno(2))
                error_num+=1
                flag = 0
        if(flag):
            symbol = ValueItem('var', 'Array', p[3], p.lineno(2))
            for x in p[1]:
                if(insert_value_table(x,symbol)):
                    print(p[3].baseType + ' ' + x, end='')
                    for i in range(0, p[3].dimension):
                        bound = p[3].period[i + 1]
                        print('[' + str(bound[1] - bound[0] + 1) + ']', end='')
                    print(';')
    else:
        symbol = ValueItem('var', p[3], None, p.lineno(2))
        for x in range(0,len(p[1])):
            if(insert_value_table(x, symbol)):
                print(p[3] + ' ' + p[1][x] + ';')
        print(';')

    # if isinstance(p[3],Array):
    #     for x in p[1]:
    #         print(p[3].baseType + ' ' + x, end='')
    #         for i in range(0, p[3].dimension):
    #             bound = p[3].period[i+1]
    #             print('['+str(bound[1]-bound[0]+1)+']', end='')
    #         print(';')
    # else:
    #     print(p[3] + ' ', end='')
    #     print(p[1][0], end='')
    #     for x in range(1, len(p[1])):
    #         print(',' + p[1][x], end='')
    #     print(';')


# type->basic_type
# 	|  array [ period  ] of basic_type
def p_type_1(p):
    '''type : basic_type'''
    p[0]=p[1]


def p_type_2(p):
    '''type : ARRAY '[' period ']' OF basic_type'''
    p[0]=Array(p[3].period, p[6])


# basic_type->integer
# 	| real
# 	|  boolean
# 	|  char
def p_basic_type_1(p):
    '''basic_type : INTEGER'''
    p[0] = 'int'


def p_basic_type_2(p):
    '''basic_type : CHAR'''
    p[0] = 'char'


def p_basic_type_3(p):
    '''basic_type : REAL'''
    p[0] = 'double'


def p_basic_type_4(p):
    '''basic_type : BOOLEAN'''
    p[0] = 'bool'


# period->period ， digits .. digits
# 	| digits .. digits
def p_period_1(p):
    '''period : period ',' NUMINT AREA NUMINT'''
    p[0] = Period(p[1].level+1, int(p[3]), int(p[5]), p[1].period)


def p_period_2(p):
    '''period : NUMINT AREA NUMINT'''
    p[0] = Period(1, int(p[1]), int(p[3]), {})


def p_idlist_1(p):
    '''idlist : idlist ',' ID'''
    p[0] = p[1]
    p[0].append(p[3])


def p_idlist_2(p):
    '''idlist : ID'''
    p[0] = []
    p[0].append(p[1])


# subprogram_declarations->subprogram_declarations subprogram ;  |  empty
def p_subprogram_declare_1(p):
    '''subprogram_declarations : subprogram_declarations subprogram ';' '''


def p_subprogram_declare_empty(p):
    '''subprogram_declarations : '''


# subprogram->subprogram_head ;  subprogram_body

def p_subprogram(p):
    '''subprogram : subprogram_head ';' subprogram_body'''
    global local_value
    local_value = {}


# subprogram_head->procedure id formal_parameter
# 		|   function  id formal_parameter :  basic_type
def p_subprogram_head_1(p):
    '''subprogram_head : PROCEDURE ID formal_parameter'''
    print('void ' + p[2], end='')
    print('(', end='')
    for group in range(len(p[3])):
        basty=p[3][group][0]
        print(basty + ' '+ p[3][group][1],end='')
        for para in range(2,len(p[3][group])):
            print(',' + basty + ' '+ p[3][group][para] ,end='')
        if(group<len(p[3])-1):
            print(',',end='')
    print(')')
    print('{')


def p_subprogram_head_2(p):
    '''subprogram_head : FUNCTION  ID formal_parameter ':'  basic_type'''
    print(p[5] + ' ' + p[2], end='')
    print('(', end='')
    for group in p[3]:
        basty = group[0]
        for para in range(1, len(group) - 1):
            print(basty + ' ' + group[para] + ', ', end='')
    print(')')
    print('{')


# formal_parameter->( parameter_list ) | empty
def p_formal_parameter_1(p):
    '''formal_parameter : '(' parameter_list ')' '''
    p[0] = p[2]


def p_formal_parameter_empty(p):
    '''formal_parameter : '''
    p[0] = []


# parameter_list->parameter_list ;  parameter |  parameter
def p_parameter_list_1(p):
    '''parameter_list : parameter_list ';'  parameter'''
    p[0]=p[1]
    p[0].append(p[3])


def p_parameter_list_2(p):
    '''parameter_list : parameter'''
    p[0]=[]
    p[0].append(p[1])

# parameter -> var_parameter | value_parameter
# var_parameter -> var value_parameter
# value_parameter -> idlist : basic_type
# subprogram_body -> const_declarations
#                   var_declarations
#                   compound_statement
# compound_statement -> begin statement_list end
# statement_list -> statement_list ; statement
#                   | statement
# statement -> variable assign expression
#                   | procedure_call
#                   | compound_statement
#                   | if expression then statement else_part
#                   | for id assign expression to expression do statement
#                   | read ( variable_list )
#                   | write ( expression_list )
#                   | empty

# parameter -> var_parameter | value_parameter
def p_parameter_1(p):
    '''parameter : var_parameter'''
    p[0] = p[1]
def p_parameter_2(p):
    '''parameter : value_parameter'''
    p[0] = p[1]

# var_parameter -> var value_parameter
def p_var_parameter_1(p):
    '''var_parameter : VAR value_parameter'''
    ls1 = p[2]
    ls1[0] = ls1[0] + '&'
    p[0] = ls1
#     print(p[2] + ';')

# value_parameter -> idlist : basic_type
def p_value_parameter_1(p):
    '''value_parameter : idlist ':' basic_type'''
    p[1].insert(0, p[3])
    p[0]=p[1]
#     p[0] = str(p[3]) + str(p[1])

# subprogram_body -> const_declarations
#                   var_declarations
#                   compound_statement
def p_subprogram_body_1(p):
    '''subprogram_body : const_declarations var_declarations compound_statement'''
    print('}')

# compound_statement -> begin statement_list end
def p_compound_statement_1(p):
    '''compound_statement : help_print_brace BEGIN statement_list END'''
    # p[0] = str(p[2])
    print('}')

def p_help_print_brace(p):
    '''help_print_brace : '''
    print('{')

# statement_list -> statement_list ; statement
#                   | statement
def p_statement_list_1(p):
    '''statement_list : statement_list ';' statement'''
    # p[0] = str(p[1]) + ';' + str(p[3])

def p_statement_list_2(p):
    '''statement_list : statement'''
    # p[0] = str(p[1])

# statement -> variable assign expression
#                   | procedure_call
#                   | compound_statement
#                   | if expression then statement else_part
#                   | for id assign expression to expression do statement
#                   | read ( variable_list )
#                   | write ( expression_list )
#                   | empty
def p_statement_1(p):
    '''statement : variable ASSIGN expression'''
    print(p[1] + '=' + p[3] + ';')

def p_statement_2(p):
    '''statement : procedure_call'''
    p[0] = str(p[1])

def p_statement_3(p):
    '''statement : compound_statement'''
    p[0] = str(p[1])

def p_statement_4(p):
    '''statement : IF expression THEN statement else_part'''
    print('if(' + p[2] + '){' + '\n' + p[4] + '\n' +'}' + '\n' + p[5])

def p_statement_5(p):
    '''statement : FOR ID ASSIGN expression TO expression DO statement'''
    print('for(' + p[2] + '=' + p[4] + ';' + p[2] + '<=' + p[6] + ';' + p[2] + '++){' + '\n' + p[8] + '\n' + '}')

def p_statement_6(p):
    '''statement : READ '(' variable_list ')' '''
    print('scanf(' + p[3] + ');')

def p_statement_7(p):
    '''statement : WRITE '(' expression_list ')' '''
    print('printf(' + p[3] + ');')

def p_statement_8(p):
    '''statement : '''
    p[0] = str('')

#variable_list-> variable_list , variable
#              | variable
#variable->id id_varpart
# id_varpart-> [ expression_list ]
#            | empty 
# procedure_call-> id
#                | id ( expression_list ) 
# else_part->else statement
#           |empty
#expression_list->expression_list , expression
#                | expression
#expression->simple_expression relop simple_expression
#           | simple_expression
#simple_expression->simple_expression addop term
#                  | term
#term->term mulop factor
#     | factor
#factor->num
#       | variable
#       | id ( expression_list )
#       | ( expression )
#       | not factor
#       | uminus factor

def p_variable_list_1(p):
    '''variable_list  : variable_list ',' variable  '''
    p[0]=str(p[0])+','+str(p[3])

def p_variable_list_2(p):
    '''variable_list  : variable'''
    p[0]=str(p[1])



def p_variable_1(p):
    '''variable :  ID id_varpart '''
    # 这是谁的呀？写的是p[0]=p[2]
    p[0] = p[1] + p[2]


def p_id_varpart_1(p):
    '''id_varpart : '[' expression_list ']' '''
    p[0]='['+str(p[2])+']'

def p_id_varpart_2(p):
    '''id_varpart : '''
    p[0]=str('')



def p_procedure_call_1(p):
    '''procedure_call : ID'''
    p[0]=p[1]

def p_procedure_call_2(p):
    '''procedure_call : ID '(' expression_list ')' '''
    p[0]=p[1]+'('+str(p[3])+')'

def p_else_part_1(p):
    '''else_part : ELSE statement '''
    p[0]=p[2]

def p_else_part_2(p):
    '''else_part : '''
    p[0]=str('')

def p_expression_list_1(p):
    '''expression_list : expression_list ',' expression'''
    p[0]=str(p[1])+','+str(p[3])

def p_expression_list_2(p):
    '''expression_list : expression '''
    p[0]=str(p[1])

def p_expression_1(p):
    '''expression : simple_expression relop simple_expression'''
    p[0]=str(p[1])+p[2]+str(p[3])

def p_expression_2(p):
    '''expression : simple_expression'''
    p[0]=str(p[1])


def p_relop(p):
    '''relop : '>'
             | '<'
             | '='
             | NOTGREATER
             | NOTLESS
             | NOTEQUAL'''
    p[0] = p[1]

def p_simple_expression_1(p):
    '''simple_expression : simple_expression addop term'''
    p[0]=str(p[1])+p[2]+str(p[3])

def p_simple_expression_2(p):
    '''simple_expression : term'''
    p[0]=str(p[1])

def p_addop(p):
    '''addop : '+'
             | '-'
             | OR'''
    p[0] = p[1]

def p_term_1(p):
    '''term : term mulop factor'''
    p[0]=str(p[1])+p[2]+str(p[3])

def p_term_2(p):
    '''term : factor'''
    p[0]=str(p[1])

def p_mulop(p):
    '''mulop : '*'
             | '/'
             | MOD
             | DIV
             | AND'''
    p[0] = p[1]

def p_factor_1(p):
    '''factor : const_value '''
    p[0]=p[1][1]

def p_factor_2(p):
    '''factor : variable'''
    p[0]= str(p[1])

def p_factor_3(p):
    '''factor : ID  '(' expression_list ')' '''
    p[0]=p[1]+'('+str(p[3])+')'

def p_factor_4(p):
    '''factor : '(' expression ')' '''
    p[0]='('+str(p[2])+')'

def p_factor_5(p):
    ''' factor : NOT factor '''
    p[0]=p[1]+str(p[2])

def p_factor_6(p):
    '''factor : '-' factor '''
    p[0]=p[1]+str(p[2])

def p_assign_1(p):
    '''assign : ASSIGN '''
    p[0]=p[1]

global_value = {}   # 全局符号表
local_value = {}    # 函数内符号表
is_global = 1       # 辅助，用于界定全局变量和内部变量

import ply.yacc as yacc

def get_Grammar():
    yacc.yacc()

ISTEST = True

if ISTEST:
    try:
        get_Grammar()
        # with open('D:/study/compiler/test_cases/test_cases/wrong_cases/test1.pas',encoding='utf-8')as f:
        with open('test3.pas', encoding='utf-8')as f:
            contents = f.read()
        yacc.parse(contents)
        if(error_num==0):
            print("grammar is true")
        for key in global_value.keys():
            global_value[key].output()
        for key in local_value.keys():
            local_value[key].output()
    except EOFError:
        print("Can't open file")

