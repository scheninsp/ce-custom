-- 采集已确认目标及管理 CE 侧实验；只写 CE Lua 数据，不写游戏内存、不调用 Run。
local state = 0x3A484D9DB60
local goods = 0x3A4012E4A60
local goodsId = 10
local tableAddress = state + 0x1D88
local base = getAddress('victoria3.exe')
local addresses = {boundary=base+0x131C2B0, add=base+0x11FD93B,
    remove=base+0x11FAF69, diagnostic=base+0x11FD5C9}
assert(debug_isDebugging() and targetIs64Bit(), 'Attached 64-bit debugger required')
local context = debug_getCurrentContextTable(false)
assert(type(context) == 'table', 'Stopped context required')
assert(readInteger(goods+0x10) == goodsId, 'Target goods ID changed')
assert(readString(goods+0x18, 5, false) == 'wood', 'Target goods key changed')

-- 生成固定原生条件；入参为事件种类与实验标识，返回 Lua 文本。
local function condition(kind, identifier)
    return string.format([=[local watch = tradeCycleAgent
if type(watch) ~= 'table' or watch.id ~= %q then return true end
-- 校验真实命中并复制事件；无入参，返回是否停下，错误由外层保存。
local ok, stop = pcall(function()
    assert(#watch.events < 10000, 'Event limit reached')
    local kind = %q
    assert(RIP == watch.addresses[kind], 'Unexpected breakpoint address')
    if kind ~= 'boundary' then
        watch.evaluations.all = watch.evaluations.all + 1
        if RCX ~= watch.tableAddress then return false end
        watch.evaluations.state = watch.evaluations.state + 1
        assert(math.type(RDX) == 'integer' and RDX ~= 0, 'Invalid goods pointer')
        local id = readInteger(RDX + 0x10)
        assert(id ~= nil, 'Cannot read goods ID')
        if id ~= watch.goodsId then return false end
        assert(RBP == 0 or RBP == 1, 'Invalid trade direction')
        assert(math.type(RBX) == 'integer' and RBX >= 0, 'Invalid quantity')
    end
    local caller = readQword(RSP)
    assert(math.type(caller) == 'integer', 'Cannot read caller')
    local event = {sequence=#watch.events+1, kind=kind, counted=watch.armed,
        ip=string.format('%%X', RIP), sp=string.format('%%X', RSP),
        thread=string.format('%%X', THREADID), caller=string.format('%%X', caller)}
    if kind ~= 'boundary' then
        event.key = kind .. '_' .. tostring(RBP)
        event.quantityRaw = tostring(RBX)
        event.goods = string.format('%%X', RDX)
        event.goodsId = watch.goodsId
        event.tableAddress = string.format('%%X', RCX)
    else
        watch.armed = false
    end
    watch.events[#watch.events+1] = event
    return true
end)
if not ok then
    watch.errors = watch.errors + 1
    watch.lastError = tostring(stop)
    return true
end
return stop]=], identifier, kind)
end

if request.action == 'test' then
    local cases = {}
    for _, name in ipairs({'boundary', 'add', 'remove', 'otherState', 'otherGoods', 'error'}) do
        local kind = name == 'boundary' and 'boundary' or (name == 'remove' and 'remove' or 'add')
        local watch = {id='offline', tableAddress=tableAddress, goodsId=goodsId, addresses=addresses,
            armed=true, events={}, errors=0, lastError='', evaluations={all=0, state=0}}
        local env = {tradeCycleAgent=watch, RIP=addresses[kind], RSP=context.RSP,
            RCX=tableAddress, RDX=goods, RBP=0, RBX=750000, THREADID=context.THREADID}
        if name == 'otherState' then env.RCX = 1 end
        if name == 'error' then env.RDX = 0 end
        if name == 'otherGoods' then
            -- 模拟不同商品 ID；入参为地址，返回固定测试 ID，不读写游戏。
            env.readInteger = function(address) return 43 end
        end
        setmetatable(env, {__index=_G})
        local chunk, compileError = load(condition(kind, 'offline'), 'trade_condition_test', 't', env)
        assert(chunk ~= nil, tostring(compileError))
        local stop = chunk()
        local filtered = name == 'otherState' or name == 'otherGoods'
        assert(stop == not filtered, 'Synthetic stop mismatch')
        assert(#watch.events == ((filtered or name == 'error') and 0 or 1), 'Synthetic event mismatch')
        assert(watch.errors == (name == 'error' and 1 or 0), 'Synthetic error mismatch')
        assert(watch.armed == (kind ~= 'boundary'), 'Synthetic armed mismatch')
        cases[#cases+1] = {name=name, ok=true}
    end
    return {ok=true, cases=cases, productionWatchUnchanged=true}
end

if request.action == 'init' then
    assert(tradeCycleAgent == nil, 'Existing experiment must not be replaced')
    assert(type(request.id) == 'string', 'Missing experiment ID')
    tradeCycleAgent = {id=request.id, tableAddress=tableAddress, goodsId=goodsId,
        addresses=addresses, armed=false, events={}, errors=0, lastError='',
        evaluations={all=0, state=0}}
    tradeCycleAgent.conditions = {}
    for _, kind in ipairs({'boundary', 'add', 'remove'}) do
        tradeCycleAgent.conditions[kind] = condition(kind, request.id)
    end
elseif request.action == 'arm' or request.action == 'disarm' then
    assert(type(tradeCycleAgent) == 'table' and tradeCycleAgent.id == request.id,
        'Experiment identity changed')
    assert(tradeCycleAgent.errors == 0, 'Experiment contains errors')
    if request.action == 'arm' then
        assert(context.RIP == addresses.boundary, 'Arm only at the boundary')
        assert(not tradeCycleAgent.armed, 'Experiment is already armed')
        assert(#tradeCycleAgent.events == tonumber(request.expectedSequence), 'Boundary sequence changed before arm')
    end
    tradeCycleAgent.armed = request.action == 'arm'
else
    assert(request.action == 'snapshot', 'Unknown watch action')
end

local storage = readQword(tableAddress+8)
local bits = readQword(tableAddress+0x20+8*(goodsId >> 6))
assert(math.type(storage) == 'integer' and math.type(bits) == 'integer', 'Unreadable goods table')
local present = (bits & (1 << (goodsId & 63))) ~= 0
local raw = '0'
if present then
    assert(storage ~= 0, 'Missing table storage')
    local value = readQword(storage+goodsId*8)
    assert(math.type(value) == 'integer', 'Unreadable goods slot')
    raw = tostring(value)
end
local result = {pid=getOpenedProcessID(), base=string.format('%X', base),
    state=string.format('%X', state), tableAddress=string.format('%X', tableAddress),
    goods=string.format('%X', goods), goodsId=goodsId, goodsKey='wood',
    capacityLimit=readInteger(state+0x1D58), capacityUsed=readInteger(state+0x1D5C),
    storage=string.format('%X', storage), present=present, capacityRaw=raw,
    context={}, addresses={}, instructions={}, watch=tradeCycleAgent or false}
for _, name in ipairs({'RIP', 'RSP', 'R14', 'RCX', 'RDX', 'RBP', 'RBX', 'THREADID'}) do
    assert(math.type(context[name]) == 'integer', 'Missing context register')
    result.context[name] = string.format('%X', context[name])
end
for kind, address in pairs(addresses) do
    result.addresses[kind] = string.format('%X', address)
    result.instructions[kind] = disassemble(address)
end
for kind, target in pairs({add=base+0x1027970, remove=base+0x1027A40}) do
    local address = addresses[kind]
    local displacement = readInteger(address+1, true)
    assert(readBytes(address, 1, false) == 0xE8 and type(displacement) == 'number'
        and address+5+displacement == target, 'Submit instruction changed')
end
local final = debug_getCurrentContextTable(false)
assert(type(final) == 'table' and final.RIP == context.RIP and final.RSP == context.RSP
    and final.THREADID == context.THREADID, 'Stopped context changed during snapshot')
return result
