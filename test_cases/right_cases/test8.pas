{正确用例}
{测试一维数组}
{输入50个数并按输入的顺序把这50个数打印出来}

program test8;
type arr=array[1..50]of integer;    {说明一数组类型arr}
var a:arr;i:integer;
begin
    write('Enter 50 integer:');
    for i:=1 to 50 do read(a[i]);   {从键盘上输入50个整数}
    for i:=1 to 50 do               {输出这50个数}
        write(a[i]);
end.