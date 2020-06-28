{正确用例}
{测试for循环}
{输出1-100之间的所有偶数}

program test7;
var i:integer;
begin
    for i:=1 to 100 do 
    if i mod 2=0 then write(i);
end.