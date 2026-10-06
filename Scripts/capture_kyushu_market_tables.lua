-- 只读采集第二次进程九州的市场系数与商品表；返回快照，不继续游戏或修改断点。
local s = 0x3E3A2D8DB60
local c = debug_getCurrentContextTable(false)
assert(getOpenedProcessID() == 12472, 'Target process changed')
assert(c and c.RIP == getAddress('victoria3.exe+1229B00') and c.R15 == s,
    'Expected Kyushu breakpoint')
local name = readString(readQword(s+0x1AD0), 100, false)
assert(name == 'HUB_NAME_STATE_KYUSHU_city_japanese', 'State identity changed')
local catalog = readQword(getAddress('victoria3.exe+50DF080')+0x18)
local count = readInteger(catalog+0x8C)
local goodsArray = readQword(catalog+0x80)
assert(count == 53, 'Goods catalog changed')

-- 读取稀疏表商品槽；入参为表地址和商品 ID，返回存在位、槽地址、原始值和有效值。
local function value(t, g)
    local bits = readQword(t+0x20+8*(g>>6))
    local slot = readQword(t+8)+8*g
    local raw = readQword(slot)
    assert(bits and raw, 'Unreadable goods table')
    local present = (bits & (1 << (g&63))) ~= 0
    return {present=present, address=string.format('%X',slot), raw=tostring(raw),
        effective=tostring(present and raw or 0)}
end

local rows = {}
for g=0,count-1 do
    local goods = readQword(goodsArray+8*g)
    assert(readInteger(goods+0x10) == g, 'Goods identity changed')
    local keyAddress = goods+0x18
    if readQword(goods+0x30)>15 then keyAddress=readQword(keyAddress) end
    rows[#rows+1] = {id=g, key=readString(keyAddress,100,false),
        c8=value(s+0xC8,g), exports=value(s+0x498,g)}
end
local final = debug_getCurrentContextTable(false)
assert(final and final.RIP==c.RIP and final.RSP==c.RSP and final.THREADID==c.THREADID,
    'Stopped context changed')
return {state=string.format('%X',s), stateId=readInteger(s+8), name=name,
    field58Address=string.format('%X',s+0x58), field58=tostring(readQword(s+0x58)),
    field68=tostring(readQword(s+0x68)), tableC8=string.format('%X',s+0xC8),
    table498=string.format('%X',s+0x498), rows=rows, context=c,
    breakpoints=debug_getBreakpointList()}
