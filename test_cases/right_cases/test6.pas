{正确用例}
{测试case语句}

program test6;
var month,days:integer;
begin
    write('Input month:');read(month);
    case month of
        1,3,5,7,8,10,12:days:=31;
        4,6,9,11:days:=30;
        2:days:=28;
        else days:=0;
    end;
    if days<>0 then write('Days=',days);
end.