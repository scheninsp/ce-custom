# 属性读取与容量相关伪代码

## `ReadModifierAttribute`（`victoria3.exe+844150`）

```cpp
// 功能：在属性容器哈希表中查找 16 位选择值并读取对应的 64 位属性。
// 入参：container 为属性容器，output 为输出地址，selector 为属性选择值；
// 返回：output 原始地址；读取不到时使用默认槽或全局默认值。
// 地址：victoria3.exe+844150。
void* ReadModifierAttribute(ModifierContainer* container, int64* output,
                            uint16 selector)
{
    HashTable* table = container->table;
    Bucket* bucket = FindBucket(table, selector);
    Entry* entry = FindEntry(bucket, selector);
    if (!entry)
        entry = DefaultEntry(container, table);
    int64 value = entry ? entry->value : ReadGlobalDefaultModifier();
    *output = value;
    return output;
}
```

