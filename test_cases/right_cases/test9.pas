{正确用例}
{测试过程}
{打印出连续n个星号并换行}

program test9;
var i:integer;
procedure draw_a_line(n:integer);
    var j:integer;
    begin
        for j:=1 to n do 
            write('*');
            write;
    end;
begin
    for i:=1 to 6 do 
        draw_a_line(i);     {调用过程，第i行打印i个连续星号}
end.