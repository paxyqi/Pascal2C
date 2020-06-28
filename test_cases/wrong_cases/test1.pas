{错误用例}
{if语句的嵌套}

program test1
var 
    x:real;
    y:integer;
begin
    write('Input x:');read(x);
    y:=0;
    if x>0 then 
        if x>0 then y:=1
    else y:=-1;     {缺少一个else}
end;