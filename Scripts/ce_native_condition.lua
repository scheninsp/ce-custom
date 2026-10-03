-- 添加、检查或比较更新原生条件执行断点；不继续目标，不删除已有断点。
local mode = request.mode or 'add'
local result = {
    ok=false, phase='preflight', created=false, conditionReadbackMatched=false,
    backend='native-ui', conditionType=request.conditionType, condition=request.condition,
    error='',
    mode=mode,
}
local timer = nil
local ownedDialog = nil

-- 校验并统一条件换行；入参为控件文本，返回保留空白的规范化文本。
local function normalizeCondition(text)
    assert(type(text) == 'string', 'Native condition text is not a string')
    return text:gsub('\r\n', '\n'):gsub('\r', '\n')
end

-- 查找唯一指定类窗体；入参为类名，返回窗体或 nil。
local function findForm(className)
    local found = nil
    for index = 0, getFormCount() - 1 do
        local form = getForm(index)
        if form.ClassName == className then
            assert(found == nil, 'Multiple matching forms')
            found = form
        end
    end
    return found
end

-- 读取必需组件；入参为窗体和组件名，返回组件，缺失时失败。
local function component(form, name)
    local control = form.findComponentByName(name)
    assert(control ~= nil, 'Missing native component: ' .. name)
    return control
end

-- 在模态循环中设置或只读条件；入参为菜单和是否写入，返回读回对象。
local function visitCondition(menu, write)
    assert(findForm('TfrmBreakpointCondition') == nil, 'Condition dialog already open')
    local observed = nil
    local failure = nil
    local began = getTickCount()
    timer = createTimer(nil, false)
    timer.Interval = 50
    -- 驱动本次条件窗口；入参为定时器，无返回值。
    timer.OnTimer = function(sender)
        -- 检查并填写本次窗口；无入参，无返回值，错误由外层捕获。
        local handled, message = pcall(function()
            local dialog = findForm('TfrmBreakpointCondition')
            if dialog == nil then
                assert(getTickCount() - began < 3000, 'Native dialog deadline exceeded')
                return
            end
            ownedDialog = dialog
            sender.Enabled = false
            local easy = component(dialog, 'rbEasy')
            local complex = component(dialog, 'rbComplex')
            local expression = component(dialog, 'edtEasy')
            local script = component(dialog, 'mComplex')
            assert(type(expression.getCaption) == 'function' and type(expression.setCaption) == 'function',
                'Native edit text API unavailable')
            assert(type(script.getCaption) == 'function' and type(script.setCaption) == 'function',
                'Native memo text API unavailable')
            if write then
                easy.Checked = request.conditionType == 'simple'
                complex.Checked = not easy.Checked
                if easy.Checked then expression.setCaption(request.condition)
                else script.setCaption(request.condition) end
            end
            local condition = nil
            if easy.Checked then condition = expression.getCaption()
            else condition = script.getCaption() end
            local normalized = normalizeCondition(condition)
            observed = {
                conditionType=easy.Checked and 'simple' or 'complex',
                condition=condition,
            }
            if write then
                assert(observed.conditionType == request.conditionType, 'Condition type write mismatch')
                assert(normalized == request.condition, 'Condition text write mismatch')
                result.conditionWriteVerified = true
            end
            dialog.ModalResult = write and 1 or 2
        end)
        if not handled then
            failure = tostring(message)
            sender.Enabled = false
            if ownedDialog ~= nil then ownedDialog.ModalResult = 2 end
        end
    end
    timer.Enabled = true
    -- 触发原生菜单事件；无入参，无返回值，窗口由 CE 创建并释放。
    local clicked, clickError = pcall(function() menu.doClick() end)
    timer.Enabled = false
    timer.destroy()
    timer = nil
    ownedDialog = nil
    assert(clicked, tostring(clickError))
    assert(failure == nil, failure)
    assert(observed ~= nil, 'Native dialog did not return condition')
    return observed
end

-- 完成查重、创建、条件保存及读回；无入参，无返回值，阶段写入局部结果。
local completed, errorText = pcall(function()
    assert(debug_isDebugging() == true, 'Debugger is not attached')
    local before = debug_getCurrentContextTable(false)
    assert(type(before) == 'table', 'No stopped context')
    assert(targetIs64Bit() == true, '64-bit target required')
    assert(request.conditionType == 'simple' or request.conditionType == 'complex', 'Invalid condition type')
    assert(mode == 'add' or mode == 'inspect' or mode == 'update', 'Invalid native condition mode')
    local address = getAddressSafe(request.address)
    assert(math.type(address) == 'integer' and address > 0, 'Cannot resolve address')
    result.address = string.format('%X', address)
    local compiled = request.conditionType == 'simple'
        and ('return (' .. request.condition .. ')') or request.condition
    local chunk, compileError = load(compiled, 'cycle_condition_compile', 't', _G)
    assert(chunk ~= nil, tostring(compileError))
    assert(findForm('TfrmBreakpointCondition') == nil, 'Condition dialog already open')
    local existingBreakpoints = debug_getBreakpointList()
    assert(type(existingBreakpoints) == 'table', 'Breakpoint list query unavailable')
    local existingMatches = 0
    for _, existing in ipairs(existingBreakpoints) do
        if existing == address then existingMatches = existingMatches + 1 end
    end
    if mode == 'add' then assert(existingMatches == 0, 'Breakpoint address already exists')
    else assert(existingMatches == 1, 'Existing breakpoint is not unique') end
    local list = findForm('TfrmBreakpointlist')
    if list == nil then
        component(getMemoryViewForm(), 'Breakpointlist1').doClick()
        list = findForm('TfrmBreakpointlist')
    end
    assert(list ~= nil, 'Breakpoint list unavailable')
    local view = component(list, 'ListView1')
    local refresh = component(list, 'Timer1').OnTimer
    local menu = component(list, 'miSetCondition')
    assert(type(refresh) == 'function', 'Breakpoint refresh unavailable')
    assert(type(createTimer) == 'function', 'Timer API unavailable')
    assert(type(getTickCount) == 'function', 'Tick API unavailable')
    if mode == 'add' then
        result.phase = 'create-attempted'
        debug_setBreakpoint(address)
    end
    local matches = 0
    local registered = debug_getBreakpointList()
    assert(type(registered) == 'table', 'Breakpoint registration query unavailable')
    for _, existing in ipairs(registered) do
        if existing == address then matches = matches + 1 end
    end
    assert(matches == 1, 'New breakpoint was not uniquely registered')
    result.created = mode == 'add'
    refresh(component(list, 'Timer1'))
    local selected = nil
    for index = 0, view.Items.Count - 1 do
        local item = view.Items[index]
        if getAddressSafe(item.Caption) == address then
            assert(selected == nil, 'Ambiguous native breakpoint row')
            selected = item
        end
    end
    assert(selected ~= nil, 'Native breakpoint row unavailable')
    result.row = {address=selected.Caption, fields={}}
    for index = 0, selected.SubItems.Count - 1 do
        result.row.fields[#result.row.fields + 1] = selected.SubItems[index]
    end
    if mode == 'update' then
        local fields = result.row.fields
        assert(fields[1] == '1' and fields[2] == 'On Execute' and fields[4] == 'Break'
            and fields[5] == 'Yes' and (fields[6] == nil or fields[6] == ''),
            'Cannot update inactive or unsupported breakpoint')
    end
    for index = 0, view.Items.Count - 1 do view.Items[index].Selected = false end
    selected.Selected = true
    if mode == 'update' then
        result.phase = 'condition-compare'
        local previous = visitCondition(menu, false)
        result.previousConditionType = previous.conditionType
        result.previousCondition = previous.condition
        assert(previous.conditionType == request.expectedType, 'Condition changed before update')
        assert(normalizeCondition(previous.condition) == request.expectedCondition, 'Condition changed before update')
    end
    if mode ~= 'inspect' then
        result.phase = 'condition-write-attempted'
        visitCondition(menu, true)
    end
    result.phase = 'condition-readback'
    local readback = visitCondition(menu, false)
    result.readbackConditionType = readback.conditionType
    result.readbackCondition = readback.condition
    local normalized = normalizeCondition(readback.condition)
    if mode ~= 'inspect' then
        assert(readback.conditionType == request.conditionType, 'Condition type mismatch')
        assert(normalized == request.condition, 'Condition text mismatch')
    end
    result.conditionReadbackMatched = true
    local after = debug_getCurrentContextTable(false)
    assert(type(after) == 'table', 'Stopped context lost')
    for _, name in ipairs({'RIP', 'RSP', 'THREADID'}) do
        assert(before[name] ~= nil and before[name] == after[name], 'Stopped context changed')
    end
    result.threadIdBefore = string.format('%X', before.THREADID)
    result.threadIdAfter = string.format('%X', after.THREADID)
    result.phase = 'completed'
    result.ok = true
end)
if timer ~= nil then timer.Enabled = false; timer.destroy(); timer = nil end
if not completed then result.error = tostring(errorText) end
return result
