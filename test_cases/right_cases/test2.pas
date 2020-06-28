{正确用例}
{测试赋值与输出}

program test2;
const   {常量说明}
    pi=3.14159;
    zero=0;
var r,c,s:real;
begin
    read(r);
    c:=2*pi*r;
    s:=pi*r*r;
    write(c);
    write(s);
end .