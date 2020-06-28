{正确用例}
{测试过程procedure和函数function}
{运行结果如下:
    *1*2
    #2#
    #2#
    ***1***2}

program test10;
var x,y:integer;
procedure a;
    var x:integer;
    begin
        x:=2;
        write('#',x,'#');
        write('#',y,'#');
    end;    {of a}
begin       {main program}
    x:=1;y:=2;
    write('*',x,'*'，y);
    a;
    write('***',x,'***',y);
end.