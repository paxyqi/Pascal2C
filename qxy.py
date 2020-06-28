error_num = 0

import ply.lex as lex  # 导入python lex模块

tokens = [
    # 关系运算符
    'NOTGREATER', 'NOTLESS', 'NOTEQUAL',
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
    'SPACE',
]

literals = ['=', '+', '-', '*', '/', '(', ')', ';', '<', '>', ',', '[', ']', ':','.']

# 关键字/保留字；本质上也可以写在tokens，但这里单独处理效率高
reserved = {
    'div':'DIV',
    'mod':'MOD',
    'and':'AND',
    'not':'NOT',
    'or':'OR',
    'var': 'VAR',
    'integer': 'INTEGER',
    'real': 'REAL',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'function': 'FUNCTION',
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

def t_SPACE(t):
    r'[ ]+'
    pass


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

# 识别数字
def t_NUMFLOAT(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)  # 返回是字符串类型，需转为float型
    return t

def t_NUMINT(t):
    r'[0-9]+'
    t.value = int(t.value)  # 返回是字符串类型，需转为整型
    return t

# ID错误情况
def t_IL_ID(t):
    r'[0-9]+[a-zA-Z]+[0-9a-zA-Z]*'
    print(f"========Illegal ID: {t.value}   line: {str(t.lineno)}")


# char常量错误情况
def t_IL_LETTER(t):
    r'\'[^\']{2}'
    print(f"========Illegal letter: {t.value}   line: {str(t.lineno)}========")







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
    print("Illegal character '%s'" % t.value[0])
    print("(%d," % t.lexer.lineno, "%d)" % t.lexer.lexpos)
    t.lexer.skip(1)

# 调用Lex模块，构建词法分析器
lexer = lex.lex()
# ===================================================================================================
# 词法测试部分
# ===================================================================================================
# # 测试输入文件与结果输出文件
# f1 = open('C:/Users/26925/Desktop/out.txt', 'w')   #输出结果
# f = open('D:/study/compiler/test_cases/test_cases/wrong_cases/test1.pas', 'r', encoding='UTF-8')
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



def p_error(p):
    global error_num
    error_num+=1
    if p:
        print("Syntax error at '%s'" %p.value," line:%d"%p.lexer.lineno)

    else:
        print("Syntax error at EOF")

def p_program_1(p):
    '''programstruct : program_head ';' program_body '.' '''

def p_program_head_1(p):
    '''program_head : PROGRAM ID '('  idlist ')' '''
def p_program_head_2(p):
    '''program_head : PROGRAM ID'''


def p_program_body_1(p):
    '''program_body :   const_declarations var_declarations subprogram_declarations compound_statement'''



def p_const_declarations_1(p):
    '''const_declarations :  CONST const_declaration ';' '''
    print('const '+p[2]+' ;')
def p_const_declarations_2(p):
    '''const_declarations :  '''
    p[0] = str('')

def p_const_declaration_1(p):#此处 c语言翻译应是const a=10，b=20； pascal是const a=10；b=20；中间的标点有不同，需要注意
    '''const_declaration :   const_declaration   ';' ID '='   const_value'''
    p[0] = str(p[1]) + ',' + p[3] + '=' + str(p[5])
def p_const_declaration_2(p):
    '''const_declaration :   ID '=' const_value'''
    p[0] = p[1]+'='+str(p[3])

def p_const_value_1(p):
    '''const_value : '+' NUMINT
                    | '-' NUMINT'''
    p[0]=p[1] + p[2]

def p_const_value_2(p):
    '''const_value : '+' NUMFLOAT
                   | '-' NUMFLOAT'''
    p[0]=p[1] + p[2]

def p_const_value_3(p):
    '''const_value :  LETTER
                   |  NUMINT
                   |  NUMFLOAT'''
    p[0] = p[1]
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


class Expr: pass


# ========================================================================
# 数组类，包括：
# dimension 数组维度，整型
# period 数组下标范围，字典型
# basictype 基本类型,str型
# ========================================================================
class Array(Expr):
    def __init__(self, period, basictype):
        self.name = 'array'
        self.baseType = basictype
        self.period = period
        self.dimension = len(period)


class Period(Expr):
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
    print(str(p[5]) + ' ' + str(p[3]) + ';')
    if isinstance(p[5],Array):
        for x in p[3]:
            print(p[5].basictype + ' ' + x, end='')
            for i in range(1, p[5].dimension):
                bound = p[5].period[i]
                print('['+str(bound[1]-bound[0]+1)+']', end='')
            print(';')
    else:
        print(str(p[3]) + ' ', end='')
        for x in p[1]:
            print(x + ', ', end='')
        print(';')


def p_var_declaration_2(p):
    '''var_declaration : idlist ':' type'''
    if isinstance(p[3],Array):
        for x in p[1]:
            print(p[3].basictype + ' ' + x, end='')
            for i in range(1, p[3].dimension):
                bound = p[3].period[i]
                print('['+str(bound[1]-bound[0]+1)+']', end='')
            print(';')
    else:
        print(p[3] + ' ', end='')
        for x in p[1]:
            print(x + ', ', end='')
        print(';')


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
    '''period : period ',' NUMINT '.' '.' NUMINT'''
    p[0] = Period(p[1].level+1, int(p[3]), int(p[6]), p[1].period)


def p_period_2(p):
    '''period : NUMINT '.' '.' NUMINT'''
    p[0] = Period(1, int(p[1]), int(p[4]), {})


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


# subprogram_head->procedure id formal_parameter
# 		|   function  id formal_parameter :  basic_type
def p_subprogram_head_1(p):
    '''subprogram_head : PROCEDURE ID formal_parameter'''
    print('void ' + p[2], end='')
    print('(', end='')
    for group in p[3]:
        basty=group[0]
        for para in range(1,len(group)-1):
            print(basty + ' '+ para + ', ',end='')
    print(')')


def p_subprogram_head_2(p):
    '''subprogram_head : FUNCTION  ID formal_parameter ':'  basic_type'''
    print(p[5] + ' ' + p[2], end='')
    print('(', end='')
    for group in p[3]:
        basty = group[0]
        for para in range(1, len(group) - 1):
            print(basty + ' ' + para + ', ', end='')
    print(')')


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

# compound_statement -> begin statement_list end
def p_compound_statement_1(p):
    '''compound_statement : BEGIN statement_list END'''
    print('int main(){\n'+str(p[2])+'}')

# statement_list -> statement_list ; statement
#                   | statement
def p_statement_list_1(p):
    '''statement_list : statement_list ';' statement'''
    p[0] = str(p[1])+'\n'  + str(p[3])
def p_statement_list_2(p):
    '''statement_list : statement'''
    p[0] = str(p[1])

# statement -> variable assign expression
#                   | procedure_call
#                   | compound_statement
#                   | if expression then statement else_part
#                   | for id assign expression to expression do statement
#                   | read ( variable_list )
#                   | write ( expression_list )
#                   | empty
def p_statement_1(p):
    '''statement : variable assign expression'''#本来在这里print
    p[0]=str(p[1]) + '=' + str(p[3]) + ';'
def p_statement_2(p):
    '''statement : procedure_call'''
    p[0] = str(p[1])
def p_statement_3(p):
    '''statement : compound_statement'''
    p[0] = str(p[1])
def p_statement_4(p):
    #if(a>2){
    #   b=1;}
    #else{ b=2;}
    '''statement : IF expression THEN statement else_part'''
    p[0]= 'if(' + str(p[2]) + '){' + '\n\t' + str(p[4]) + '}' + '\n' +str(p[5])
def p_statement_5(p):
    '''statement : FOR ID assign expression TO expression DO statement'''
    p[0]='for('+str(p[2])+'='+str(p[4])+ ';' + str(p[2]) + '<=' + str(p[6]) + ';' + str(p[2]) + '++){' + '\n' + str(p[8]) + '\n}'
def p_statement_6(p):
    '''statement : READ '(' variable_list ')' '''#scanf("%d",&r);
    p[0]='scanf("%d",&'+str(p[3])+ ');'
def p_statement_7(p):
    '''statement : WRITE '(' expression_list ')' '''#printf("%d",p);
    p[0]='printf("%d",'+str(p[3])+');'
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

def p_else_part_1(p):#if(){}else{}
    '''else_part : ELSE statement '''
    p[0]='else{\n\t'+str(p[2])+'}'
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

def p_mulop_1(p):
    '''mulop : '*'  '''
    p[0] = p[1]

def p_mulop_2(p):
    '''mulop : '/'
             | DIV  '''
    p[0] = '/'

def p_mulop_3(p):
    '''mulop : MOD '''
    p[0] = '%'

def p_mulop_4(p):
    '''mulop : AND'''
    p[0] = '&'

def p_factor_1(p):
    '''factor : const_value '''
    p[0]=p[1]

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

import ply.yacc as yacc

def get_Grammar():
    yacc.yacc()

ISTEST = True

if ISTEST:
    try:
        get_Grammar()
        with open('C:/Users/pixy/OneDrive/3.5/编译原理/code/test_cases/right_cases/c1.pas',encoding='utf-8')as f:
            contents = f.read()
        yacc.parse(contents)
        if(error_num==0):
            print("grammar is true")
    except EOFError:
        print("Can't open file")

