{正确用例}
{判断输入的数是否为偶数}
{测试简单的分支语句}

program test4;
var a,b,c:integer;
begin
    read(a);
    b:=0;
    c:=1;
    if a=0 then a:=c 
    else a:=b;
    write(a);
end.