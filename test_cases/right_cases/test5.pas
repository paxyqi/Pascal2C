{正确用例}
{测试if语句的嵌套}

program test5;
var x:real;
    y:integer;
begin
    read(x);
    if x>0 then y:=1    {x>0时，y的值为1}
        else            {x<=0时}  
            if x=0 then y:=0
            else y:=-1;
    write(y);
end.